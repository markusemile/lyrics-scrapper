from pydantic import BaseModel
from typing import List


class SongModel(BaseModel):
    id: int
    artist_id: int
    title: str
    filename: str


class ArtistModel(BaseModel):
    id: int
    name: str
    songs: List[SongModel]


class ArtistWrapper(BaseModel):
    artist: ArtistModel
