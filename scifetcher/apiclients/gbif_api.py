import os
import logging as log
import requests
from scifetcher.apiclients.base_api import BaseApi

INCLUDE_GBIF_SEARCH = os.getenv("INCLUDE_GBIF_SEARCH") == "True"


class GbifApi(BaseApi):
    def get_gbif_search(self):
        log.debug(f"get_gbif_search: {self.query}...")
        response = requests.get(
            "http://api.gbif.org/v1/species/search?q={}&limit=6".format(self.query)
        )
        if response.status_code == 200:
            data = response.json()
            if data and data["count"] > 0:
                summary = "GBIF SEARCH:\nResult: {}\n".format(data["count"])
                for data in data["results"]:
                    summary += "{} {} | {} | {} | Taxonrank: {} > {} > {} > {} > {} > {} > {}\n".format(
                        data.get("taxonomicStatus"),
                        data.get("rank"),
                        data.get("canonicalName"),
                        data.get("authorship"),
                        data.get("kingdom"),
                        data.get("phylum"),
                        data.get("class"),
                        data.get("order"),
                        data.get("family"),
                        data.get("genus"),
                        data.get("species"),
                    )
                log.debug("found!")
                return summary.strip()
            else:
                log.debug("notfound!")
                return "Not Found"
        else:
            log.debug("error!")
            return "Error"

    def get_scientific_name(self):
        log.debug(f"get_scientific_name: {self.query}...")
        args = {"q": self.query, "language": "en"}
        response = requests.get("http://api.gbif.org/v1/species/search", params=args)
        if response.status_code == 200:
            data = response.json()
            for result in data["results"]:
                species = result.get("species")
                if species:
                    log.debug("found!")
                    return species
        log.debug("notfound!")
        return self.query

    def get_gbif_match(self):
        log.debug(f"get_gbif_match: {self.query}...")
        response = requests.get(
            "http://api.gbif.org/v1/species/match?name={}".format(self.query)
        )
        if response.status_code == 200:
            data = response.json()
            if data["matchType"] != "NONE":
                if data.get("rank") != "SPECIES":
                    log.debug("notfound!")
                    return self.get_gbif_search(self.query)
                else:
                    log.debug("found!")
                    return "GBIF MATCH: {} {} | {} {} | {} | {}\nTaxonrank: {} > {} > {} > {} > {} > {} > {}".format(
                        data.get("matchType"),
                        data.get("confidence"),
                        data.get("status"),
                        data.get("rank"),
                        data.get("canonicalName"),
                        data.get("authorship"),
                        data.get("kingdom"),
                        data.get("phylum"),
                        data.get("class"),
                        data.get("order"),
                        data.get("family"),
                        data.get("genus"),
                        data.get("species"),
                    )
            elif INCLUDE_GBIF_SEARCH:
                return self.get_gbif_search(self.query)
            else:
                log.debug("notfound!")
                return "Not Found"
        else:
            log.debug("error!")
            return "Error"

