# Semantic Search Engine (Elasticsearch + NLP)

A simple semantic search engine that retrieves relevant products based on meaning rather than exact keyword matches using dense vector embeddings.

## Tech Stack
- Python
- Elasticsearch
- Sentence Transformers (SBERT)
- Pandas

## Features
- Indexes product catalog data
- Generates semantic embeddings for product descriptions
- Performs vector-based semantic search
- Secure credential handling using environment variables

## Setup

### Clone Repository
```bash
git clone https://github.com/sonuj04/Private-Proj.git
cd semantic_search
```


## Install Dependencies
```
pip install -r requirements.txt
```

## Configuration

This project requires Elasticsearch credentials to be provided via **environment variables**.  

### Required Environment Variables

| Variable Name | Description |
|--------------|-------------|
| `ES_URL` | Elasticsearch cluster URL |
| `ES_USERNAME` | Elasticsearch username |
| `ES_PASSWORD` | Elasticsearch password |
| `ES_CA_CERT` | Path to Elasticsearch CA certificate |

### Using a `.env` File (Recommended)

Create a `.env` file in the project root :

```env
ES_URL=https://localhost:9200
ES_USERNAME=elastic
ES_PASSWORD=your_password
ES_CA_CERT=/path/to/http_ca.crt
```