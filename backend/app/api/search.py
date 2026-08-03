from fastapi import APIRouter
import time

from app.core.elastic import get_es_client
from app.core.model import get_embedding_model
from app.schemas.search import SearchRequest, SearchResponse
from app.core.model import get_embedding_model, get_cross_encoder


def reciprocal_rank_fusion(bm25_hits, knn_hits, k: int = 60):
    """
    Combines two ranked result lists using Reciprocal Rank Fusion.
    """
    scores: dict[str, float] = {}
    docs: dict[str, dict] = {}

    for rank, hit in enumerate(bm25_hits):
        doc_id = hit["_id"]
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
        docs[doc_id] = hit

    for rank, hit in enumerate(knn_hits):
        doc_id = hit["_id"]
        scores[doc_id] = scores.get(doc_id, 0) + 1.0 / (k + rank + 1)
        docs[doc_id] = hit

    ranked_ids = sorted(scores, key=scores.get, reverse=True)
    return [docs[doc_id] for doc_id in ranked_ids]

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
def search(req: SearchRequest):
    start_total = time.perf_counter()

    es = get_es_client()
    model = get_embedding_model()
    start=time.perf_counter()
    # Encode query
    query_vector = model.encode(
        req.query,
        normalize_embeddings=True
    ).tolist()
    encoding_time = (time.perf_counter() - start)

    # Build filters
    filters = []

    if req.gender is not None and req.gender != "ALL":
        filters.append({"term": {"Gender": req.gender}})

    filters.append({
        "range": {
            "Price (INR)": {
                "lte": req.max_price
            }
        }
    })
    start=time.perf_counter()
    # Hybrid search (rrf combines bm25+knn rankings instead of summing raw scores (which lets bm25 dominate since its scores are unbounded while knn is 0-1))
    bm25_res = es.search(
        index="all_products",
        query={
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": req.query,
                            "fields": [
                                "ProductName^2",
                                "Description",
                                "ProductBrand",
                                "Gender"
                            ]
                        }
                    }
                ],
                "filter": filters
            }
        },
        size=100,
        _source=[
            "ProductName",
            "ProductBrand",
            "Gender",
            "Price (INR)",
            "Description"
        ]
    )

    knn_res = es.search(
        index="all_products",
        knn={
            "field": "DescriptionVector",
            "query_vector": query_vector,
            "k": 100,
            "num_candidates": 1000,
            "filter": filters
        },
        size=100,
        _source=[
            "ProductName",
            "ProductBrand",
            "Gender",
            "Price (INR)",
            "Description"
        ]
    )
    retrieval_time = (time.perf_counter() - start)
    hits = reciprocal_rank_fusion(bm25_res["hits"]["hits"], knn_res["hits"]["hits"])


    cross_encoder = get_cross_encoder()
    start = time.perf_counter()
    pairs = [
    (req.query, f"{hit['_source']['ProductName']}. {hit['_source']['Description']}")
    for hit in hits
]

    scores = cross_encoder.predict(pairs)
    rerank_time = (time.perf_counter() - start)

    scored_hits = list(zip(hits, scores))

    scored_hits.sort(key=lambda x: x[1], reverse=True)
    top_hits = [hit for hit, _ in scored_hits[:10]]


    results = [
        {
            "ProductName": hit["_source"]["ProductName"],
            "ProductBrand": hit["_source"]["ProductBrand"],
            "Gender": hit["_source"]["Gender"],
            "Price": hit["_source"]["Price (INR)"],
            "Description": hit["_source"]["Description"],
        }
        for hit in top_hits
    ]
    return {
        "results": results,
        "latency_ms": {
            "total": round((time.perf_counter() - start_total) * 1000, 2),
            "encoding": round(encoding_time * 1000, 2),
            "retrieval": round(retrieval_time * 1000, 2),
            "reranking": round(rerank_time * 1000, 2),
        }
    }
