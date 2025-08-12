import os
from dotenv import load_dotenv
from enum import Enum


load_dotenv()

API_BASIC_PATH = os.getenv("API_BASE_URL")
TOKEN = os.getenv("TOKEN")

headers = {
    "Authorization": "Bearer "+TOKEN
}


class KeyValue(Enum):
    KEY = "key"
    VALUE = "value"


class ApiPaths(Enum):
    SEARCH = os.getenv("API_SEARCH")
    API_ARTISTS = os.getenv("API_ARTISTS")
    DISCO = os.getenv("API_DISCOGRAPHY")
    SONG = os.getenv("API_SONG")


