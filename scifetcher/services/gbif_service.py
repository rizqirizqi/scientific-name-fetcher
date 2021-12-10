import re
import logging as log
import requests
from scifetcher.config import ENV_CONFIG
from scifetcher.helpers.list import list_get
from scifetcher.helpers.scientific import threat_status_name_to_symbol
from scifetcher.helpers.string import clean_encode_query, fuzzy_search
from scifetcher.models.species import Species
from scifetcher.services.base_service import BaseService


class GbifService(BaseService):

    SEARCH_LIMIT = 100

    def fetch_data(self, query, description=None):
        species_list = []
        try:
            # Get data from query
            species_list = self.fetch_gbif_search(query)
            # Get data from similar query
            if (
                len(species_list) <= 0
                and ENV_CONFIG["AUTO_SEARCH_SIMILAR_SPECIES"]
                and description != None
            ):
                similar_name = fuzzy_search(description, query)
                if similar_name and query != similar_name:
                    species_list = self.fetch_gbif_search(similar_name)
            # Get data from first word
            if len(species_list) <= 0 and query.split()[0] != query:
                species_list = self.fetch_gbif_search(query.split()[0])
        except Exception as e:
            log.error(f"[Error] {query} {e}")
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
            for item in data["results"]:
                # filter constituentKey and taxonID to get backbone only result
                # https://www.gbif.org/developer/species#p_datasetKey
                if not "constituentKey" in item:
                    continue
                if "taxonID" in item:
                    continue
                species_list.append(
                    Species(
                        source="GBIF",
                        id=item.get("key"),
                        url=f"https://www.gbif.org/species/{item.get('key')}",
                        search_url=f"https://www.gbif.org/species/search?q={clean_encode_query(query)}",
                        taxonomic_status=item.get("taxonomicStatus"),
                        rank=item.get("rank"),
                        accepted_name=item.get("accepted"),
                        scientific_name=item.get("scientificName"),
                        canonical_name=item.get("canonicalName"),
                        authorship=item.get("authorship"),
                        taxon_kingdom=item.get("kingdom"),
                        taxon_phylum=item.get("phylum"),
                        taxon_class=item.get("class"),
                        taxon_order=item.get("order"),
                        taxon_family=item.get("family"),
                        taxon_genus=item.get("genus"),
                        taxon_species=item.get("species"),
                        threat_status=threat_status_name_to_symbol(
                            list_get(item.get("threatStatuses"), 0, "")
                        ),
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
                        source="GBIF",
                        id=data.get("key"),
                        url=f"https://www.gbif.org/species/{data.get('key')}",
                        search_url=f"https://www.gbif.org/species/search?q={clean_encode_query(query)}",
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
                        threat_status=threat_status_name_to_symbol(
                            list_get(data.get("threatStatuses"), 0, "")
                        ),
                        match_type=data.get("matchType"),
                        match_confidence=data.get("confidence"),
                    )
                ]
        elif ENV_CONFIG["INCLUDE_GBIF_SEARCH"]:
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
