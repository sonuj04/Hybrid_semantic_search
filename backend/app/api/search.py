from fastapi import APIRouter
import time

from app.core.elastic import get_es_client
from app.core.model import get_embedding_model
from app.schemas.search import SearchRequest, SearchResponse
from app.core.model import get_embedding_model, get_cross_encoder

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
def search(req: SearchRequest):
    start_time = time.time()

    es = get_es_client()
    model = get_embedding_model()

    # Encode query
    query_vector = model.encode(
        req.query,
        normalize_embeddings=True
    )

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

    # Hybrid search
    res = es.search(
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
        knn={
            "field": "DescriptionVector",
            "query_vector": query_vector,
            "k": 100,
            "num_candidates": 1000
        },
        _source=[
            "ProductName",
            "ProductBrand",
            "Gender",
            "Price (INR)",
            "Description"
        ]
    )
    hits = res["hits"]["hits"]
    cross_encoder = get_cross_encoder()

    pairs = [
        (req.query, hit["_source"]["Description"])
        for hit in hits
    ]

    scores = cross_encoder.predict(pairs)

    # Attach scores
    scored_hits = list(zip(hits, scores))

    # Sort by cross-encoder score (descending)
    scored_hits.sort(key=lambda x: x[1], reverse=True)

    # Take top 10
    top_hits = [hit for hit, _ in scored_hits[:10]]

    latency_ms = (time.time() - start_time) * 1000

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
        "latency_ms": latency_ms
    }
