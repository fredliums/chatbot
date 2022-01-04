"""
Example script to create elasticsearch documents.
"""
import argparse
import json

import pandas as pd
from bert_serving.client import BertClient
bc = BertClient(output_fmt='list')

def create_document(doc, index_name, emb=""):
    ret = {
        '_op_type': 'index',
        '_index': index_name,
        'text': doc['text'],
        'title': doc['title']
    }
    if emb:
        ret["vector"] = emb

    return ret


def load_dataset(path):
    docs = []
    df = pd.read_csv(path)
    for row in df.iterrows():
        series = row[1]
        doc = {
            'title': series.Question,
            'text': series.Answer
        }
        docs.append(doc)
    return docs


def bulk_predict(docs, batch_size=256):
    """Predict bert embeddings."""
    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i: i+batch_size]
        embeddings = bc.encode([doc['title'] for doc in batch_docs])
        for emb in embeddings:
            yield emb


def main(args):
    strategy = 'semantic' if args.index_name == 'semantic' else 'pattern'
    docs = load_dataset(args.data)
    with open(args.save, 'w') as f:
        if strategy == 'pattern':
            for doc in docs:
                d = create_document(doc, args.index_name)
                f.write(json.dumps(d) + '\n')
        else:
            for doc, emb in zip(docs, bulk_predict(docs)):
                d = create_document(doc, args.index_name, emb)
                f.write(json.dumps(d) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creating elasticsearch documents.')
    parser.add_argument('--data', help='data for creating documents.')
    parser.add_argument('--save', help='created documents.')
    parser.add_argument('--index_name', default='pattern', help='Elasticsearch index name.')
    args = parser.parse_args()
    main(args)
