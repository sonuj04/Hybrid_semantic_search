# Semantic Search Engine 

A semantic search engine that retrieves relevant products based on meaning rather than just exact keyword matches. 

Traditional keyword search fails when users describe products differently than how they're listed. This engine uses Hybrid BM25 + kNN retrieval with smart filter first architecture for production scale performance.

## Tech Stack
- Python
- FastAPI
- Elasticsearch 8.15 (Docker)
- SentenceTransformers
- CrossEncoder 
- Streamlit
- Pydantic
- Uvicorn

## Features
- SBERT embeddings capture meaning, not just keywords
- Offline indexing + real time retrieval
- Combines exact matching with vector similarity.
- Cross-Encoder reranking for precision boost
- Secure credential handling using environment variables
- Efficient querying on large datasets
- Clean FastAPI REST API
- Modular Architecture with separation of concerns

## Performance considerations
- Embeddings normalized for cosine similarity optimization
- Filter first reduces search space
- Cross encoder applied to top 100 retrieved candidates to control latency
- Offline embedding generation (only once needed)

## Architecture

```
┌───────────────────────────────────────────────────────┐
│                   Frontend (streamlit ui)             │
│                                                       │
└───────────────────────────────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────┐
│              Backend(fastAPI API Layer)               │
│                                                       │
│search logic + embedding model + elasticsearch client  │
│  Cross encoder reranking of 100 retrieved products    │
└───────────────────────────────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────┐
│                     Search layer                      │
│              (elasticsearch embeddings)               │
└───────────────────────────────────────────────────────┘
                              ↓
┌───────────────────────────────────────────────────────┐
│   Data (embedding generation using bulk indexing)     │
│     (indexed vectors from ingestion pipeline)         │
└───────────────────────────────────────────────────────┘
```


## Setup

### Prerequisites
- Docker and Docker Compose
- Python 3.12
- ~5GB free disk space for Elasticsearch + models

### 1. Clone the repository
```bash
git clone https://github.com/sonuj04/Hybrid_semantic_search.git
cd Hybrid_semantic_search
```

### 2. Start Elasticsearch

This project runs Elasticsearch in Docker with security (TLS + authentication) enabled by default.

```bash
docker compose up -d
docker compose logs -f elasticsearch
```

Wait for `"started"` in the logs, then stop watching with `Ctrl+C`. The container generates its own TLS certificate on first boot.

### 3. Extract the CA certificate and set the password

```bash
mkdir -p certs
docker cp elasticsearch:/usr/share/elasticsearch/config/certs/http_ca.crt ./certs/http_ca.crt

docker exec -it elasticsearch /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic -a -b
```

Copy the password printed by the reset command — you'll need it in the next step.

### 4. Create your `.env` file

Copy the example and fill in your values:
```bash
cp .env.example .env
```

```env
ES_URL=https://localhost:9200
ES_USERNAME=elastic
ES_PASSWORD=<password from step 3>
ES_CA_CERT=/absolute/path/to/Hybrid_semantic_search/certs/http_ca.crt
```

> **Important:** `ES_CA_CERT` must be an **absolute path**. It's read by code running from different working directories (ingestion notebook, backend server), so a relative path will resolve incorrectly and fail depending on where the process is launched from.

Verify the connection:
```bash
curl --cacert ./certs/http_ca.crt -u elastic:<password> https://localhost:9200
```
You should get back a JSON response with `"tagline": "You Know, for Search"`.

### 5. Create a Python virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate

cd backend && pip install -r requirements.txt && cd ..
cd frontend && pip install -r requirements.txt && cd ..
```

### 6. Index the data (one-time setup)

Place `myntra_products_catalog.csv` in the project root (see [Dataset](#dataset) below), then:

```bash
cd ingestion
pip install jupyter
jupyter notebook indexData.ipynb
```

Run all cells top to bottom. This creates the `all_products` index with the correct vector mapping and bulk-indexes ~10,000 product embeddings.

### 7. Run the backend

```bash
cd backend
uvicorn app.main:app --reload
```

Check `http://localhost:8000/health` — should return `{"status":"healthy"}`.

### 8. Run the frontend

```bash
cd frontend
streamlit run searchApp.py
```

Open `http://localhost:8501` and search.

## Dataset

Download `myntra_products_catalog.csv` and place it in the project root before running ingestion.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ES_URL` | Elasticsearch cluster URL |
| `ES_USERNAME` | Elasticsearch username |
| `ES_PASSWORD` | Elasticsearch password |
| `ES_CA_CERT` | **Absolute** path to the CA certificate |