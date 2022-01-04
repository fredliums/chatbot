# Elasticsearch meets BERT

Below is a job search example:

![An example of bertsearch](./docs/example.png)

## System architecture

![System architecture](./docs/architecture.png)

## Requirements
- python3
- pip3
- Docker
- Docker Compose >= [1.22.0](https://docs.docker.com/compose/release-notes/#1220)

## Getting Started

### 1. Prepare

This will download pretrained BERT models, set environment and install reqiured packages

```bash
$ source ./prepare
```

### 2. Run Docker containers


```bash
$ docker-compose up -d
```

**CAUTION**: If possible, assign high memory(more than `8GB`) to Docker's memory configuration because BERT container needs high memory.

### 3. Prepare data

You can use the create index API to add a new index to an Elasticsearch cluster. Once you created an index, you’re ready to index some document. After converting your data into a JSON, you can adds a JSON document to the specified index and makes it searchable. So there are three steps:

* Create indexes
* Create documents
* Index documents

```bash
$ ./prepare_data
```

### 4. Open browser

Go to <http://127.0.0.1:5050>.


[（Chotbot项目说明文档）](https://github.com/yangz12dell/chatbot/blob/main/docs/chatbot.md)
