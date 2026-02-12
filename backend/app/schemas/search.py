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


class SearchResponse(BaseModel):
    results: List[Product]
    latency_ms: float
