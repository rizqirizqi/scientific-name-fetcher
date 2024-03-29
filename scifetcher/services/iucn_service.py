import re
import logging as log
import requests
from scifetcher.config import ENV_CONFIG
from scifetcher.helpers.concurrent import run_concurrently
from scifetcher.models.species import Species
from scifetcher.helpers.list import list_get
from scifetcher.helpers.string import clean_encode_query, fuzzy_search
from scifetcher.services.base_service import BaseService


class IucnService(BaseService):
    def fetch_data(self, query, description=None):
        species_list = []
        try:
            # Get data from query
            species_list = self.search_species(query)
            # Get data from similar query
            if (
                len(species_list) <= 0
                and ENV_CONFIG["AUTO_SEARCH_SIMILAR_SPECIES"]
                and description != None
            ):
                similar_name = fuzzy_search(description, query)
                if similar_name and query != similar_name:
                    species_list = self.search_species(similar_name)
        except Exception as e:
            log.error(f"[Error] {query} {e}")
        return species_list

    def search_species(self, query):
        log.debug(f"search_species: {query}...")
        # CASES:
        # Gardenia longiflora: synonym
        # Derris scandedns: synonym
        # Aporusa fusiformis: synonym
        # Wrightia pubescens: 2 synonym > web result 3 > fetch original_species
        [species_list, ori_species_result, ori_species_url] = run_concurrently(
            [
                (self.fetch_synonym, query),
                (self.fetch_species, query),
                (self.fetch_species_url, query),
            ]
        )
        if ori_species_result and ori_species_result.get("taxonid"):
            original_species = self.create_species_from_result(
                query, ori_species_result, ori_species_url
            )
            species_list.insert(0, original_species)
        if len(species_list) <= 0:
            log.debug("notfound!")
            return []
        for idx, species in enumerate(species_list):
            if ori_species_result and idx == 0:
                continue
            [species_result, species_url] = run_concurrently(
                [
                    (self.fetch_species, species.canonical_name),
                    (self.fetch_species_url, species.canonical_name),
                ]
            )
            species = self.create_species_from_result(
                species.canonical_name, species_result, species_url, species
            )
        log.debug("found!")
        return species_list

    def fetch_species_url(self, query):
        log.debug(f"fetch_species_url: {query}...")
        response = requests.get(
            f"https://apiv3.iucnredlist.org/api/v3/weblink/{clean_encode_query(query)}",
        )
        data = response.json()
        if not data or not data.get("rlurl"):
            log.debug("notfound!")
            return None
        log.debug("found!")
        return data["rlurl"]

    def fetch_species(self, query):
        log.debug(f"fetch_species: {query}...")
        params = {"token": ENV_CONFIG["IUCN_API_TOKEN"]}
        response = requests.get(
            f"https://apiv3.iucnredlist.org/api/v3/species/{clean_encode_query(query)}",
            params=params,
        )
        data = response.json()
        if not data or len(data.get("result") or []) <= 0:
            log.debug("notfound!")
            return None
        if data.get("species"):
            log.debug("notfound!")
            return None
        species_result = data.get("result")[0]
        log.debug("found!")
        return species_result

    def fetch_synonym(self, query):
        log.debug(f"fetch_synonym: {query}...")
        params = {"token": ENV_CONFIG["IUCN_API_TOKEN"]}
        response = requests.get(
            f"https://apiv3.iucnredlist.org/api/v3/species/synonym/{clean_encode_query(query)}",
            params=params,
        )
        data = response.json()
        if not data or len(data.get("result") or []) <= 0:
            log.debug("notfound!")
            return []
        species_list = []
        for species_result in data.get("result") or []:
            species = self.create_species_from_result(query, species_result)
            species_list.append(species)
        log.debug("found!")
        return species_list

    def create_species_from_result(
        self, query, species_result=None, species_url=None, species: Species = None
    ):
        if not species:
            species = Species()
            species.source = "IUCN"
            species.canonical_name = query
            species.rank = "SPECIES"
        if species_result and species_result.get("accepted_id"):
            species.id = species_result.get("accepted_id")
            species.scientific_name = f"{species_result.get('synonym')} {species_result.get('syn_authority')}".strip()
            species.accepted_name = f"{species_result.get('accepted_name')} {species_result.get('authority')}".strip()
            species.canonical_name = species_result.get("accepted_name")
        if species_result and species_result.get("taxonid"):
            species.id = species_result.get("taxonid")
            if not species.scientific_name:
                species.scientific_name = f"{species_result.get('scientific_name')} {species_result.get('authority')}".strip()
            if not species.accepted_name:
                species.accepted_name = f"{species_result.get('scientific_name')} {species_result.get('authority')}".strip()
            species.canonical_name = species_result.get("scientific_name")
            species.authorship = species_result.get("authority")
            species.taxon_kingdom = species_result.get("kingdom")
            species.taxon_phylum = species_result.get("phylum")
            species.taxon_class = species_result.get("class")
            species.taxon_order = species_result.get("order")
            species.taxon_family = species_result.get("family")
            species.taxon_genus = species_result.get("genus")
            species.taxon_species = species_result.get("scientific_name")
            species.threat_status = species_result.get("category")
        if species_url:
            species.url = species_url
        return species
