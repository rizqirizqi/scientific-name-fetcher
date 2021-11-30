import os
import re
import logging as log
import requests
from scifetcher.helpers.list import list_get
from scifetcher.models.species import Species
from scifetcher.services.base_service import BaseService

INCLUDE_GBIF_SEARCH = os.getenv("INCLUDE_GBIF_SEARCH") == "True"
AUTO_SEARCH_SIMILAR_SPECIES = os.getenv("AUTO_SEARCH_SIMILAR_SPECIES") == "True"


class GbifService(BaseService):
    def fetch_data(self, query, description):
        self.query = query
        self.description = description
        species_list = []
        try:
            # Get GBIF Data from name
            species_list = self.fetch_gbif_match(query)
            # Get GBIF Data from similar name
            if (
                species_list == None
                and AUTO_SEARCH_SIMILAR_SPECIES
                and description != None
            ):
                match = re.findall(query.split()[0] + " [a-z]+", description)
                similar_name = list_get(match, 0)
                if similar_name:
                    species_list = self.fetch_gbif_match(similar_name)
            # Get GBIF Data from first word
            if species_list == None and query.split()[0] != query:
                species_list = self.fetch_gbif_match(query.split()[0])
        except:
            log.error("error!")
        return species_list

    def fetch_gbif_search(self, query):
        log.debug(f"fetch_gbif_search: {query}...")
        params = {"q": query, "limit": 6}
        response = requests.get(f"http://api.gbif.org/v1/species/search", params=params)
        data = response.json()
        species_list = []
        if data and data["count"] > 0:
            for data in data["results"]:
                species_list.append(
                    Species(
                        "GBIF",
                        taxonomic_status=data.get("taxonomicStatus"),
                        rank=data.get("rank"),
                        canonical_name=data.get("canonicalName"),
                        authorship=data.get("authorship"),
                        taxon_kingdom=data.get("kingdom"),
                        taxon_phylum=data.get("phylum"),
                        taxon_class=data.get("class"),
                        taxon_order=data.get("order"),
                        taxon_family=data.get("family"),
                        taxon_genus=data.get("genus"),
                        taxon_species=data.get("species"),
                        description=self.description,
                    )
                )
            log.debug("found!")
        else:
            log.debug("notfound!")
        return species_list

    def fetch_gbif_match(self, query):
        log.debug(f"fetch_gbif_match: {query}...")
        response = requests.get(f"http://api.gbif.org/v1/species/match?name={query}")
        data = response.json()
        if data["matchType"] != "NONE":
            if data.get("rank") != "SPECIES":
                log.debug("notfound!")
                return self.fetch_gbif_search(query)
            else:
                log.debug("found!")
                return [
                    Species(
                        "GBIF",
                        taxonomic_status=data.get("status"),
                        rank=data.get("rank"),
                        canonical_name=data.get("canonicalName"),
                        authorship=data.get("authorship"),
                        taxon_kingdom=data.get("kingdom"),
                        taxon_phylum=data.get("phylum"),
                        taxon_class=data.get("class"),
                        taxon_order=data.get("order"),
                        taxon_family=data.get("family"),
                        taxon_genus=data.get("genus"),
                        taxon_species=data.get("species"),
                        match_type=data.get("matchType"),
                        match_confidence=data.get("confidence"),
                        description=self.description,
                    )
                ]
        elif INCLUDE_GBIF_SEARCH:
            return self.fetch_gbif_search(query)
        else:
            log.debug("notfound!")
            return []

    def fetch_scientific_name(self, query):
        log.debug(f"fetch_scientific_name: {query}...")
        params = {"q": query, "language": "en"}
        response = requests.get("http://api.gbif.org/v1/species/search", params=params)
        data = response.json()
        for result in data["results"]:
            species = result.get("species")
            if species:
                log.debug("found!")
                return species
        log.debug("notfound!")
        return query
