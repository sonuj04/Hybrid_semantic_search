# Semantic Search Engine 

A semantic search engine that retrieves relevant products based on meaning rather than just exact keyword matches. Traditional keyword search fails when users describe products differently than how they're listed. This engine uses Hybrid BM25 + kNN retrieval with smart filter first architecture for somewhat production scale performance.

## Tech Stack
- Python
- Elasticsearch
- Sentence Transformers (SBERT)
- Pandas
- Streamlit

## Features
- SBERT embeddings capture meaning, not just keywords
- Offline indexing + real time retrieval
- Combines exact matching with vector similarity.
- Secure credential handling using environment variables
- Efficient querying on large datasets



## Architecture

```
┌────────────────────────────────────────────────────┐
│            Layer 1: Offline Ingestion              │
│                (indexData.ipynb)                   │
│                                                    │
│  CSV → Cleaning → Embeddings → Bulk Indexing → ES  │
│                                                    │
│  • SentenceTransformer (used once offline)         │
│  • Bulk indexing for efficiency                    │
│  • Dense vector storage (DescriptionVector)        │
│                                                    │
│  WHY OFFLINE? Embedding generation is expensive    │
│               Data doesn't change per query        │
│               Keeps online search fast             │
└────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────┐
│              Layer 2: Retrieval Layer              │
│                     (searchApp.py)                 │
│                                                    │
│  User Query → Encode → Filters → ES Hybrid Search  │
│                                                    │
│  HYBRID RETRIEVAL STRATEGY:                        │
│  • BM25: Exact keywords, brands, attributes        │
│  • kNN: Semantic intent, paraphrases, vague queries│
│  • Filters (Gender, Price): Applied FIRST in ES    |
│  Order: Filters → Relevance → Ranking              │
└────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────┐
│             Layer 3: UI Layer                      │
│           (searchApp.py - Streamlit)               │
└────────────────────────────────────────────────────┘
```


## Setup

# Clone Repository
```bash
git clone https://github.com/sonuj04/Private-Proj.git
cd semantic_search
```


# Install Dependencies
```
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
# Run the indexing pipeline
jupyter notebook indexData.ipynb
```

### Run the Application

```bash
streamlit run searchApp.py
```

Open your browser to `http://localhost:8501`

---


## Roadmap

- [ ] Add support for image search (CLIP embeddings)
- [ ] Implement query expansion for better recall
- [ ] Add A/B testing framework for ranking experiments
- [ ] Multi-language support
- [ ] Redis caching for frequent queries
- [ ] Docker containerization
- [ ] RESTful API endpoint (FastAPI)

---