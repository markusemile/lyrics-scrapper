from pydantic import BaseModel
from typing import List


class Result(BaseModel):
    id: int
    full_title: str
    url: str


class Song(BaseModel):
    result: Result


class Songs(BaseModel):
    songs: List[Result]
    next_page: int


class Meta(BaseModel):
    status: int


class ArtSongsResponse(BaseModel):
    meta: Meta
    response: Songs


