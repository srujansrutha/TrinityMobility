from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = "default"

class QueryResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]
    timestamp: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    content: str
    metadata: Dict[str, Any]
    score: float