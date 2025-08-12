import msvcrt
import pathlib

from app_model import SongModel
from app_model.disco_response import Songs, Song
from app_model.search_response import Responses
from app_model.response_model import ResponseModel
from typing import List, Dict
from app_utils.log_logger import get_logger
from app_utils.paginate_data import paginate_data
from pprint import pprint
from app_service import ApiService
from decorators import validate_return
from config import KeyValue
from typing import Union
from app_utils.color import error, info
from app_utils.wipe_screen import wipe_screen
from app_service.lyrics_scrapper import LyricService
from app_service import FileService


class Artist:

    def __init__(self, artist_id: int | None = None, artist_name: str | None = None):
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.artist_songs: List[SongModel] = []
        self.logger = get_logger()
        self.logger.debug("Initialisation of Artist")
        self.api_service = ApiService()
        self.lyric_service = LyricService()
        self.file_service = FileService()

    def if_no_data(self, q: ResponseModel, key_to_check: str = "data", log_msg: str = "data was not found into query"):
        value = getattr(q, key_to_check, None)
        if not value:
            self.logger.error(log_msg)
            return None

    @validate_return(context="Artist/set_name")
    def set_name(self, art_name: str | None = None, **kwargs) -> str:
        """
        Define the name of the artist we want to find
        :param expected_type: str
        :param art_name: str
        :return: str
        """
        logger = self.logger

        if isinstance(art_name, str) and len(art_name) > 0:
            self.artist_name = art_name.lower()
            self.logger.debug(f"name is {self.artist_name} ")
            return self.artist_name

        if art_name is None:
            while True:
                wipe_screen()
                entered_name = input("Please enter the name of the artist: ").strip().lower()
                if entered_name:
                    self.artist_name = entered_name
                    self.logger.debug(f"name is {self.artist_name} ")
                    return self.artist_name
                else:
                    self.logger.debug(f"name is {self.artist_name} ")
                    input("Please enter a name.  [ENTER] to try again")
                    continue

    @validate_return(context="Artist/get_id_artist")
    def get_id_artist(self, artist: str | None = None, **kwargs):
        if artist is None:
            if self.artist_name is None:
                while self.artist_name is None:
                    self.set_name()

        self.artist_name = artist
        self.logger.debug(f"make request to [api_service]/[find_artist] with args: artist= {artist}")
        artists_found = dict()

        while True:
            query = self.api_service.find_artist(artist=artist)
            self.if_no_data(q=query, log_msg="Data not found into query")

            hits = Responses(**query.data).hits

            self.if_no_data(q=query, key_to_check="hits", log_msg="Hits not found into query or empty")

            for hit in hits:
                artist_obj = getattr(hit.result, "primary_artist", None)

                if artist_obj and self.artist_name in hit.result.primary_artist.name.lower():
                    artists_found[artist_obj.id] = artist_obj.name
                else:
                    self.logger.error(f"can't find result or primary_artist and name into {hit}")

            if not artists_found:
                self.logger.error("artist found is empty")
                info("We find no name, please try with other artist !")
                input("[enter]")
                artist = self.set_name(expected_type=str)
            else:
                break

        self.logger.debug("pass list to paginatedData")

        choice = paginate_data(
            dico=artists_found,
            title="Choice between this artists",
            hint_to_display=KeyValue.VALUE,
            hint_to_return=KeyValue.KEY,
            expected_type=Union[str, None]
        )

        if choice is None:
            return None

        self.artist_id = int(choice)
        return int(choice)

    @validate_return(context="Artist/get_discography")
    def get_discography(self, art_id: int | None = None, page: int = 1, **kwargs) -> Songs | None:

        if art_id is None:
            self.logger.error("You must give a artist ID to get discography")
            return None

        self.logger.debug(f"make request to [api_service]/[find_artist_songs] with args: ID= {art_id}")
        query = self.api_service.find_artist_songs(artist_id=art_id, page=page)

        self.if_no_data(q=query)

        songs = Songs(**query.data)

        if not songs:
            self.logger.error("songs was empty")
            return None

        return songs

    @validate_return(context="Artist/get_url_song_from_disco")
    def get_url_song_from_discography(self, songs: Songs, page: int = 1, **kwargs) -> str | None:
        while True:
            if not isinstance(songs, Songs):
                self.logger.error("songs was not a Songs instance")
                raise Exception("songs is not a Songs instance")

            next_page = songs.next_page
            all_songs = songs.songs
            song_list: Dict[int, str] = dict()
            list_to_display: Dict[int, str] = dict()
            list_of_url: Dict[int, str] = dict()

            for v in all_songs:
                list_to_display[v.id] = v.full_title
                list_of_url[v.id] = v.url

            choice: str = paginate_data(
                dico=list_to_display,
                hint_to_display=KeyValue.VALUE,
                hint_to_return=KeyValue.KEY,
                title="Choose you song",
                page=page,
                expected_type=Union[str, None],
                next_page=next_page)

            if choice == "next":
                page = next_page
                songs = self.get_discography(
                    art_id=self.artist_id,
                    expected_type=Union[Songs, None],
                    page=page
                )
                continue
            elif choice == "prev":
                page = page - 1
                songs = self.get_discography(
                    art_id=self.artist_id,
                    expected_type=Union[Songs, None],
                    page=page
                )
                continue
            elif choice is None:
                return None
            else:
                return list_of_url[int(choice)]

    def get_lyric_from_url(self, url: str | None = None, attr: str | None = None, **kwargs) -> str | None:
        if url is None:
            error("You need to specified an url and a attribute to scrape a web page !")
            return None

        ly_service = self.lyric_service
        returned_lyrics = ly_service.scrapper(url=url, attr="data-exclude-from-selection")
        if returned_lyrics:
            self.display_lyrics(returned_lyrics)

    def display_lyrics(self, a):
        while True:
            wipe_screen()
            print(f"Artist: {self.artist_name}")
            print(a)

            choice = input("""
            [s] to save lyrics into your songs
            [x] to exit to main menu
            """).strip().lower()
            if choice == "x":
                return None
            elif choice == "s":
                fs = self.file_service
                fs.save_file(name=self.artist_name, content=a)
                return True
            else:
                continue
