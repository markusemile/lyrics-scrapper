from app_class import Artist
from app_model.disco_response import Songs
from typing import Union
from app_utils import wipe_screen
from app_utils.color import error

menu = """
[1] Search song by Artist
[2] Search song by title
[3] Show my saved songs
[4] Analyse a songs of Artist

[0] Exit

Choose between [1,2,3,4 or 0] : 
"""

while True:
    wipe_screen()
    choice = input(menu)
    match choice:
        case "1":
            a = Artist()
            artist_name: str = a.set_name(expected_type=str)
            artist_id = a.get_id_artist(artist=artist_name, expected_type=Union[int, None])
            if artist_id is None:
                continue
            discography = a.get_discography(art_id=artist_id, expected_type=Union[Songs, None])
            if discography is None:
                continue
            song = a.get_url_song_from_discography(songs=discography, expected_type=Union[str, None])
            if song is None:
                continue
            a.get_lyric_from_url(url=song)


print("end")


