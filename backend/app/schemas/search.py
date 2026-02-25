from pydantic import BaseModel
from typing import List,Optional


class SearchRequest(BaseModel):
    query: str
    gender: Optional[str] = None
    max_price: int = 10000


class Product(BaseModel):
    ProductName: str
    ProductBrand: str
    Gender: str
    Price: int
    Description: str

class LatencyBreakdown(BaseModel):
    total: float
    encoding: float
    retrieval: float
    reranking: float
class SearchResponse(BaseModel):
    results: List[dict]
    latency_ms: LatencyBreakdown
