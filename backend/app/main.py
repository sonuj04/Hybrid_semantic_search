from fastapi import FastAPI
from app.api.search import router as search_router
from app.core.elastic import get_es_client

app = FastAPI(
    title="Fashion Semantic Search API"
)

app.include_router(search_router)


@app.get("/health")
def health():
    try:
        es = get_es_client()
        es_healthy = es.ping()
    except Exception:
        es_healthy = False

    return {
        "status": "healthy" if es_healthy else "degraded",
        "elasticsearch": es_healthy
    }