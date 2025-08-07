from typing import List
from enum import Enum

from pydantic import BaseModel, Field

from licitabot.domain.entities import SearchResult


class SearchInputType(str, Enum):
    TEXT = "text"
    EMBEDDING = "embedding"


class SearchRequest(BaseModel):
    input: str | List[float] = Field(..., description="Input to search for")
    input_type: SearchInputType = Field(..., description="Type of input")


class SearchResponse(BaseModel):
    results: List[SearchResult] = Field(..., description="Search results")
