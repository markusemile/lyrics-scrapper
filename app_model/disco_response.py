from typing import List, Optional
from pydantic import BaseModel


class Song(BaseModel):
    id: int
    full_title: str
    url: str


class Songs(BaseModel):
    songs: List[Song]
    next_page: Optional[int]


class Meta(BaseModel):
    status: int


class DiscographyResponse(BaseModel):
    meta: Meta
    response: Songs
