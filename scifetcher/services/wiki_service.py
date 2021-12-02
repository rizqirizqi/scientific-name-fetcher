import requests
import logging as log
from scifetcher.helpers.list import list_get
from scifetcher.helpers.string import fuzzy_search


class WikiService:
    def fetch_data(self, query):
        self.query = query
        try:
            description = self.fetch_description()
            if description != None:
                return description
            reco_keyword = self.get_recommended_keyword()
            if reco_keyword != None:
                description = f"Do you mean: {reco_keyword}"
        except Exception as e:
            log.error(f"error! {e}")
            description = "Error, please retry."
        return description

    def get_recommended_keyword(self):
        log.debug(f"get_recommended_keyword: {self.query}...")
        params = {"action": "opensearch", "search": self.query}
        response = requests.get(
            f"https://commons.wikimedia.org/w/api.php", params=params
        )
        data = response.json()
        if list_get(data[1], 0):
            log.debug("found!")
            return list_get(data[1], 0)
        else:
            log.debug("notfound!")
            return None

    def fetch_description(self):
        log.debug(f"get_description: {self.query}...")
        params = {
            "action": "query",
            "prop": "extracts",
            "exlimit": "max",
            "format": "json",
            "exsentences": "2",
            "origin": "*",
            "exintro": "true",
            "explaintext": "true",
            "generator": "search",
            "gsrsearch": self.query,
        }
        response = requests.get("https://en.wikipedia.org/w/api.php", params=params)
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
            return None
