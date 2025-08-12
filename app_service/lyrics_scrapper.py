import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class LyricService:

    def __init__(self):
        self.url = None
        self.attr = None

    def scrapper(self, url: str | None = None, attr: str | None = None) -> str:
        """
        function to scrape a page in regards of the given attribute
        :param url: str -> page to scrap
        :param attr: str -> the name of the attributes to search into the page
        :return: return the text to scrape
        """
        if url is None or attr is None:
            raise Exception("Scrapper function need a url and a attributes to scap a page")

        self.url = url
        self.attr = attr

        query = requests.get(url)
        raw_content = query.content
        soup = BeautifulSoup(raw_content, "html.parser")
        lyrics_container = soup.find("div", attrs={"data-lyrics-container": "true"})
        raw_title = lyrics_container.find_next("h2").text
        title = raw_title[:-7]
        first_child_div = lyrics_container.find("div", recursive=False)
        if first_child_div:
            first_child_div.decompose()
        lyrics = lyrics_container.get_text(separator="\n", strip=True)
        return f"{title}\n{lyrics}"
