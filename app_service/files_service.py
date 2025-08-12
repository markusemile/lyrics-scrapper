import unicodedata
import json
from pathlib import Path
import re
import os
from app_utils import error, info


class FileService:
    def __init__(self):
        self.racine = Path(__file__).parent.parent.resolve()

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

        index_file = self.racine / "lyrics" / "index.json"

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
        path = self.racine / "lyrics" / name

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
                fp = self.racine / "lyrics" / name / f"{title}.txt"
                rel_fp = str(fp.relative_to(self.racine / "lyrics"))
                self.update_songs_file(artist=name, title=title, file_path=rel_fp)
                info("Lyrics was saved successfully")
                return True
        except IOError as e:
            raise Exception(e)


if __name__ == "__main__":
    fs = FileService()

