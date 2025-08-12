import unicodedata
import json
import re
import os
from typing import Any, Union, Text
from pathlib import Path
from app_utils import error, info
from app_utils.paginate_data import paginate_data, KeyValue
from pydantic import BaseModel
from app_utils import wipe_screen


class LocalSongModel(BaseModel):
    title: str
    path: str


class FileService:
    def __init__(self):
        self.racine = Path(__file__).parent.parent.resolve()
        self.lyrics_folder = self.racine / "lyrics"
        self.index_file = self.lyrics_folder / "index.json"

    @staticmethod
    def safe_folder_name(pathname: str):

        max_length = 20

        if pathname is None:
            raise Exception("Bad request: folder name required")

        # normalize accents
        name = unicodedata.normalize("NFKD", pathname)
        name = "".join(c for c in name if not unicodedata.combining(c))

        # replace restricted characters
        name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name)

        # remove the spaces
        name = re.sub(r"\s+", "_", name).strip()

        # Avoid windows reserved names (case-insensitive)
        reserved = {
            "CON", "PRN", "AUX", "NUL",
            *(f"COM{i}" for i in range(1, 10)),
            *(f"LPT{i}" for i in range(1, 10))

        }
        if name.upper() in reserved:
            name = f"_{name}_"

        if len(name) > max_length:
            name = name[:max_length].rstrip()

        return name

    def update_songs_file(self, artist: str, title: str, file_path: str):

        index_file = self.index_file

        if index_file.exists():
            with open(index_file, "r", encoding="utf8") as f:
                index_data = json.load(f)
        else:
            index_data = {}

        if artist not in index_data:
            index_data[artist] = []

        song_entry = {"title": title, "path": str(file_path)}
        if song_entry not in index_data[artist]:
            index_data[artist].append(song_entry)

        try:
            with open(index_file, "w", encoding="utf8")as f:
                json.dump(index_data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            raise Exception(e)

    def save_file(self, name: str, content: str):

        if name is None or content is None:
            raise Exception("Bad request, parameters missing")

        name = self.safe_folder_name(name)
        path = self.lyrics_folder / name

        try:
            path.mkdir(parents=True, exist_ok=True)
        except IOError as e:
            raise Exception(e)

        title = content.splitlines()[0] if content else "no_title"
        title = self.safe_folder_name(title)
        file_path = path / f"{title}.txt"

        if os.path.exists(file_path):
            choice = error("Warning !! File exist do you want to overwrite ? [y] or [n]")
            if choice != "y":
                error("lyrics was not saved !!")
                return None

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                fp = self.lyrics_folder / name / f"{title}.txt"
                rel_fp = str(fp.relative_to(self.lyrics_folder))
                self.update_songs_file(artist=name, title=title, file_path=rel_fp)
                info("Lyrics was saved successfully")
                return True
        except IOError as e:
            raise Exception(e)

    def get_list_of_artist(self):
        index_file = self.index_file

        if not index_file.exists():
            error("Index not exist. Please add first one lyric\n[Enter] to continue...")

        with open(index_file, "r", encoding="utf-8") as f:
            try:
                index_data: [LocalSongModel] = json.load(f)
            except json.JSONDecodeError as e:
                if e.msg.lower() == "expecting value":
                    error("No data into file ! please add first some lyrics.     \n[Enter] to continue")
                return None
        sorted_artist = dict(sorted(index_data.items()))
        return sorted_artist

    def show_my_file(self):
        """
         display file with paginator
         can select an artist and song after that
         can read , edit or deleted the song
        """

        my_datas = self.get_list_of_artist()

        if my_datas is None:
            return
        while True:
            choice_artist: str = paginate_data(
                dico=my_datas,
                page=1,
                hint_to_display=KeyValue.KEY,
                hint_to_return=KeyValue.KEY,
                expected_type=Union[Text, None]
            )

            if choice_artist is None:
                info("Return to the main menu [Enter] to continue")
                break

            artist_songs: [LocalSongModel] = my_datas.get(choice_artist)
            song_to_display = {i: song['title'] for i, song in enumerate(artist_songs)}
            song_kv = {song["title"]: song["path"] for song in artist_songs}
            choice_song = paginate_data(
                dico=song_to_display,
                page=1,
                hint_to_display=KeyValue.VALUE,
                hint_to_return=KeyValue.VALUE,
                expected_type=Union[Text, None]
            )
            if choice_song is None:
                info("Cancel by user [Enter] to continue")
                return

            song_path = self.lyrics_folder / song_kv[choice_song]

            if not song_path.exists():
                error(f"{song_path} not exist, check your json file !")
                return None

            with open(song_path, "r", encoding="utf-8") as f:
                lyrics = f.read()
                wipe_screen()
                print(lyrics)
                info("[enter] to return to main menu")
                continue
        return


if __name__ == "__main__":
    fs = FileService()


