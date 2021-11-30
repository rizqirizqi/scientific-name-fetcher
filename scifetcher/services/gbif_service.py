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

    SEARCH_LIMIT = 6

    def fetch_data(self, query, description):
        self.query = query
        species_list = []
        try:
            # Get GBIF Data from name
            species_list = self.fetch_gbif_search(query)
            # Get GBIF Data from similar name
            if (
                len(species_list) <= 0
                and AUTO_SEARCH_SIMILAR_SPECIES
                and description != None
            ):
                match = re.findall(query.split()[0] + " [a-z]+", description)
                similar_name = list_get(match, 0)
                if similar_name:
                    species_list = self.fetch_gbif_search(similar_name)
            # Get GBIF Data from first word
            if len(species_list) <= 0 and query.split()[0] != query:
                species_list = self.fetch_gbif_search(query.split()[0])
        except:
            log.error("error!")
        return species_list

    def fetch_gbif_search(self, query):
        log.debug(f"fetch_gbif_search: {query}...")
        params = {
            "q": query,
            "limit": self.SEARCH_LIMIT,
            "locale": "en",
            "advanced": "false",
            "facet": "rank",
            "facet": "dataset_key",
            "facet": "constituent_key",
            "facet": "highertaxon_key",
            "facet": "name_type",
            "facet": "status",
            "facet": "issue",
            "facet": "origin",
            "issue.facetLimit": 100,
            "name_type.facetLimit": 100,
            "rank.facetLimit": 100,
            "status.facetLimit": 100,
            "facetMultiselect": "true",
        }
        response = requests.get(f"http://api.gbif.org/v1/species/search", params=params)
        data = response.json()
        species_list = []
        if data and data["count"] > 0:
            for data in data["results"]:
                encoded_query = re.sub(r"[^\w]", " ", query).strip().replace(" ", "%20")
                species_list.append(
                    Species(
                        source="GBIF",
                        id=data.get("key"),
                        url=f"https://www.gbif.org/species/{data.get('key')}",
                        search_url=f"https://www.gbif.org/species/search?q={encoded_query}",
                        taxonomic_status=data.get("taxonomicStatus"),
                        rank=data.get("rank"),
                        accepted_name=data.get("accepted"),
                        scientific_name=data.get("scientificName"),
                        canonical_name=data.get("canonicalName"),
                        authorship=data.get("authorship"),
                        taxon_kingdom=data.get("kingdom"),
                        taxon_phylum=data.get("phylum"),
                        taxon_class=data.get("class"),
                        taxon_order=data.get("order"),
                        taxon_family=data.get("family"),
                        taxon_genus=data.get("genus"),
                        taxon_species=data.get("species"),
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
                encoded_query = re.sub(r"[^\w]", " ", query).strip().replace(" ", "%20")
                return [
                    Species(
                        source="GBIF",
                        id=data.get("key"),
                        url=f"https://www.gbif.org/species/{data.get('key')}",
                        search_url=f"https://www.gbif.org/species/search?q={encoded_query}",
                        taxonomic_status=data.get("status"),
                        rank=data.get("rank"),
                        accepted_name=data.get("accepted"),
                        scientific_name=data.get("scientificName"),
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
