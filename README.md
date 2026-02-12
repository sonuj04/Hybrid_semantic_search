# Semantic Search Engine 

A semantic search engine that retrieves relevant products based on meaning rather than just exact keyword matches. Traditional keyword search fails when users describe products differently than how they're listed. This engine uses Hybrid BM25 + kNN retrieval with smart filter first architecture for somewhat production scale performance.

## Tech Stack
- Python
- FastAPI
- Elasticsearch 8.x
- SentenceTransformers
- Streamlit
- Pydantic
- Uvicorn

## Features
- SBERT embeddings capture meaning, not just keywords
- Offline indexing + real time retrieval
- Combines exact matching with vector similarity.
- Secure credential handling using environment variables
- Efficient querying on large datasets
- Clean FastAPI REST API
- Modular Architecture with separation of concerns



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
│                                                       │
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

# Clone Repository
```bash
git clone https://github.com/sonuj04/Private-Proj.git
cd semantic_search
```


# Install Dependencies
```
cd backend
pip install -r requirements.txt
cd ../frontend
pip install -r requirements.txt
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

