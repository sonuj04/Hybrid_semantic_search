# Semantic Search Engine 

A semantic search engine that retrieves relevant products based on meaning rather than just exact keyword matches. 

Traditional keyword search fails when users describe products differently than how they're listed. This engine uses Hybrid BM25 + kNN retrieval with smart filter first architecture for production scale performance.

## Tech Stack
- Python
- FastAPI
- Elasticsearch 8.x
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

### Clone Repository
```bash
git clone https://github.com/sonuj04/Private-Proj.git
cd semantic_search
```
### Create venv
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```
cd backend
pip install -r requirements.txt
cd ../frontend
pip install -r requirements.txt
cd ..
```

## Configuration

Create a `.env` file in the project root:

```env
ES_URL=https://localhost:9200
ES_USERNAME=elastic
ES_PASSWORD=your_password
ES_CA_CERT=/path/to/http_ca.crt
```

**Environment Variables:**

| Variable | Description | 
|----------|-------------|
| `ES_URL` | Elasticsearch cluster URL | 
| `ES_USERNAME` | Elasticsearch username | 
| `ES_PASSWORD` | Elasticsearch password | 
| `ES_CA_CERT` | Path to CA certificate (for HTTPS) |



## Data Indexing (One-Time Setup)

```bash
cd ingestion
jupyter notebook indexData.ipynb
```

### Run Backend

```bash
cd backend
uvicorn app.main:app --reload
```

### Run Frontend
```bash
cd frontend
streamlit run searchApp.py
```

Open your browser to `http://localhost:8501`

---

