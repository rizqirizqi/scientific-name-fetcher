import requests
import logging as log
from scifetcher.helpers.list import list_get
from scifetcher.helpers.string import fuzzy_search
from scifetcher.apiclients.base_api import BaseApi


class WikiApi(BaseApi):
    def get_recommended_keyword(self):
        log.debug(f"get_recommended_keyword: {self.query}...")
        response = requests.get(
            "https://commons.wikimedia.org/w/api.php?action=opensearch&search={}".format(
                self.query
            )
        )
        data = response.json()
        if list_get(data[1], 0):
            log.debug("found!")
            return list_get(data[1], 0)
        else:
            log.debug("notfound!")
            return "Not Found"

    def get_description(self):
        log.debug(f"get_description: {self.query}...")
        response = requests.get(
            "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exlimit=max&format=json&exsentences=2&origin=*&exintro=&explaintext=&generator=search&gsrsearch={}".format(
                self.query
            )
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("query"):
                pages = data["query"]["pages"].values()
                sorted_pages = sorted(list(pages), key=lambda item: item["index"])
                extracts = ""
                for p in sorted_pages:
                    if any(s in p["title"].lower() for s in ["index of", "list of"]):
                        continue
                    if fuzzy_search(p["extract"], self.query):
                        extracts += p["extract"] + "\n"
                log.debug("found!")
                return extracts.strip()
            else:
                log.debug("notfound!")
                return "Not Found"
        else:
            log.debug("error!")
            return "Error"
