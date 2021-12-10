import logging as log
import pykew.powo as powo
from scifetcher.config import ENV_CONFIG
from scifetcher.helpers.string import clean_encode_query, fuzzy_search
from scifetcher.models.species import Species
from scifetcher.services.base_service import BaseService


class PowoService(BaseService):
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
        response = powo.search(query)
        if response.size() <= 0:
            log.debug("notfound!")
            return []
        species_list = []
        for item in response:
            taxonStatus = ""
            accepted_name = ""
            scientific_name = ""
            if item.get("accepted"):
                taxonStatus = "ACCEPTED"
                scientific_name = f"{item.get('name')} {item.get('author')}".strip()
                accepted_name = f"{item.get('name')} {item.get('author')}".strip()
            elif "synonymOf" in item:
                taxonStatus = "SYNONYM"
                scientific_name = f"{item.get('name')} {item.get('author')}".strip()
                accepted_name = f"{item['synonymOf'].get('name')} {item['synonymOf'].get('author')}".strip()
            species = Species()
            species.source = "POWO"
            species.id = item.get("fqId")
            species.url = f"https://powo.science.kew.org/{item.get('url')}"
            species.search_url = (
                f"https://powo.science.kew.org/results?q={clean_encode_query(query)}"
            )
            species.taxonomic_status = taxonStatus
            species.rank = item.get("rank")
            species.accepted_name = accepted_name
            species.scientific_name = scientific_name
            species.canonical_name = item.get("name")
            species.authorship = item.get("author")
            species.taxon_kingdom = item.get("kingdom")
            species.taxon_family = item.get("family")
            species.taxon_genus = item.get("name").split()[0]
            species.taxon_species = item.get("name")
            species.match_confidence = 0
            species_list.append(species)
        log.debug("found!")
        return species_list
