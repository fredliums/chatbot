import os
from pprint import pprint

from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from bert_serving.client import BertClient
SEARCH_SIZE = 10

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def analyzer():
    client = Elasticsearch('elasticsearch:9200')

    question = request.args.get('question')
    strategy = request.args.get('strategy')

    if strategy != 'semenitic':
        strategy = 'pattern'

    if strategy == 'pattern':
        query = {
            "query_string": {
                "default_field": "title",
                "query": question,
                "escape": True
            }
        }
    else:
        bc = BertClient(ip='bertserving', output_fmt='list')
        query_vector = bc.encode([question])[0]
        query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, doc['vector']) + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }

    #pprint(query)
    response = client.search(
        index=strategy,
        body={
            "size": SEARCH_SIZE,
            "query": query,
            "_source": {"includes": ["title", "text"]}
        }
    )

    #pprint(response)
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
