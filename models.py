from pydantic import BaseModel, Field
from typing import List,Optional


class Search(BaseModel):
    text: str = Field("Mr", description="The text to search")
    top_k: Optional[int] = Field(10, description="The number of results to return")
    threshold: Optional[float] = Field(0.5, description="The minimum similarity threshold")


class SearchResults(BaseModel):
    id: str
    content: str
    score: float


class SearchResponse(BaseModel):
    query: str
    results: List[SearchResults]
    top_k: int
    threshold: float


class User(BaseModel):
    user_id: str
    request_count: int
