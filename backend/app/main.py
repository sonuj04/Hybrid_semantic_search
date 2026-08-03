from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.search import router as search_router
from app.core.elastic import get_es_client
from app.core.model import get_embedding_model, get_cross_encoder


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_embedding_model()
    get_cross_encoder()
    yield


app = FastAPI(
    title="Fashion Semantic Search API",
    lifespan=lifespan
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