import requests
from config import API_BASIC_PATH, ApiPaths, headers
from app_utils.log_logger import get_logger
from decorators import validate_response
from pprint import pprint
from app_model.response_model import ResponseModel


class ApiService:

    def __init__(self):
        self.base_path = API_BASIC_PATH
        self.logger = get_logger()
        self.logger.debug("initialisation of ApiService")

    @validate_response(expected_type=ResponseModel)
    def find_artist(self, artist: str | None = None):

        if artist is None:
            self.logger.error("No artist name passed into service")
            raise Exception("You must give a artist name to search his ID")

        layout_path = API_BASIC_PATH + ApiPaths.SEARCH.value
        path = layout_path.replace("[:term]", artist)
        self.logger.debug(f"Make request at {path}")
        query = requests.get(path, headers=headers)
        return query

    @validate_response(expected_type=ResponseModel)
    def find_artist_songs(self, artist_id: int | None = None, page: int = 1, per_page: int = 10):

        if artist_id is None:
            self.logger.error("No artist ID passed into service")
            raise Exception("You must give a artist ID to search his ID")

        layout_path = API_BASIC_PATH + ApiPaths.DISCO.value
        path = layout_path.replace("[:id]", str(artist_id))
        self.logger.debug(f"Make request at {path}")
        query = requests.get(path, headers=headers, params={"per_page": per_page, "page": page})
        return query



