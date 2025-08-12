from pydantic import BaseModel
from typing import List


class PrimaryArtist(BaseModel):
    id: int
    name: str


class Result(BaseModel):
    full_title: str
    url: str
    primary_artist: PrimaryArtist


class Hit(BaseModel):
    result: Result


class Responses(BaseModel):
    hits: List[Hit]


class Meta(BaseModel):
    status: int


class SearchResponse(BaseModel):
    meta: Meta
    response: Responses


