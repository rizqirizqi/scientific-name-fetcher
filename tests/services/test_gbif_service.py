import responses
from unittest import TestCase, main as test_main
from requests import Timeout
from unittest.mock import patch
from scifetcher.config import ENV_CONFIG
from scifetcher.models.species import Species
from scifetcher.services.gbif_service import GbifService


@patch.dict(
    "scifetcher.config.ENV_CONFIG", {"AUTO_SEARCH_SIMILAR_SPECIES": "True"}, clear=True
)
class TestGbifService(TestCase):

    description = "Parkia speciasa (the bitter bean, twisted cluster bean, or stink bean) is a plant of the genus Parkia in the family Fabaceae.  It bears long, flat edible beans with bright green seeds the size and shape of plump almonds which have a rather peculiar smell, similar to, but stronger than that of the shiitake mushroom, due to sulfur-containing compounds also found in shiitake, truffles and cabbage."

    @responses.activate
    def test_fetch_data_success_gbif_search(self):
        responses.add(
            responses.GET,
            "http://api.gbif.org/v1/species/search?q=Parkia+speciosa&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
            json={
                "count": 3,
                "results": [
                    {
                        "key": 1,
                        "constituentKey": 1,
                        "taxonomicStatus": "ACCEPTED",
                        "rank": "SPECIES",
                        "scientificName": "Parkia speciosa Hassk.",
                        "canonicalName": "Parkia speciosa",
                        "authorship": "Hassk.",
                        "kingdom": "Viridiplantae",
                        "phylum": "Streptophyta",
                        "class": "Magnoliopsida",
                        "order": "Fabales",
                        "family": "Fabaceae",
                        "genus": "Parkia",
                        "species": "Parkia speciosa",
                    },
                    {
                        "key": 2,
                        "taxonomicStatus": "ACCEPTED",
                        "rank": "SPECIES",
                        "scientificName": "Parkia speciosa",
                        "canonicalName": "Parkia speciosa",
                        "authorship": "",
                        "kingdom": "Viridiplantae",
                        "phylum": "Streptophyta",
                        "class": "Magnoliopsida",
                        "order": "Fabales",
                        "family": "Fabaceae",
                        "genus": "Parkia",
                        "species": "Parkia speciosa",
                    },
                    {
                        "key": 3,
                        "constituentKey": 3,
                        "taxonID": 3,
                        "taxonomicStatus": "ACCEPTED",
                        "rank": "SPECIES",
                        "scientificName": "Parkia speciosa",
                        "canonicalName": "Parkia speciosa",
                        "authorship": "",
                        "kingdom": "Viridiplantae",
                        "phylum": "Streptophyta",
                        "class": "Magnoliopsida",
                        "order": "Fabales",
                        "family": "Fabaceae",
                        "genus": "Parkia",
                        "species": "Parkia speciosa",
                    },
                ],
            },
            status=200,
        )
        gbif_species_list = GbifService().fetch_data(
            "Parkia speciosa", self.description
        )
        self.assertEqual(len(gbif_species_list), 1)
        self.assertEqual(
            gbif_species_list[0],
            Species(source="GBIF", id=1, scientific_name="Parkia speciosa Hassk."),
        )

    @responses.activate
    def test_fetch_data_success_similar_name(self):
        responses.add(
            responses.GET,
            "http://api.gbif.org/v1/species/search?q=Parkia+speciosa&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
            json={"count": 0,},
            status=200,
        )
        responses.add(
            responses.GET,
            "http://api.gbif.org/v1/species/search?q=Parkia+speciasa&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
            json={
                "count": 1,
                "results": [
                    {
                        "key": 1,
                        "constituentKey": 1,
                        "taxonomicStatus": "ACCEPTED",
                        "rank": "SPECIES",
                        "scientificName": "Parkia speciasa Asa.",
                        "canonicalName": "Parkia speciasa",
                        "authorship": "Asa.",
                        "kingdom": "Viridiplantae",
                        "phylum": "Streptophyta",
                        "class": "Magnoliopsida",
                        "order": "Fabales",
                        "family": "Fabaceae",
                        "genus": "Parkia",
                        "species": "Parkia speciasa",
                    },
                ],
            },
            status=200,
        )
        gbif_species_list = GbifService().fetch_data(
            "Parkia speciosa", self.description
        )
        self.assertEqual(len(gbif_species_list), 1)
        self.assertEqual(
            gbif_species_list[0],
            Species(source="GBIF", id=1, scientific_name="Parkia speciasa Asa."),
        )

    @responses.activate
    def test_fetch_data_success_genus(self):
        responses.add(
            responses.GET,
            "http://api.gbif.org/v1/species/search?q=Parkia+speciosa&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
            json={"count": 0,},
            status=200,
        )
        responses.add(
            responses.GET,
            "http://api.gbif.org/v1/species/search?q=Parkia&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
            json={
                "count": 1,
                "results": [
                    {
                        "key": 1,
                        "constituentKey": 1,
                        "taxonomicStatus": "ACCEPTED",
                        "rank": "GENUS",
                        "scientificName": "Parkia",
                        "canonicalName": "Parkia",
                        "kingdom": "Viridiplantae",
                        "phylum": "Streptophyta",
                        "class": "Magnoliopsida",
                        "order": "Fabales",
                        "family": "Fabaceae",
                        "genus": "Parkia",
                    },
                ],
            },
            status=200,
        )
        gbif_species_list = GbifService().fetch_data("Parkia speciosa", None)
        self.assertEqual(len(gbif_species_list), 1)
        self.assertEqual(
            gbif_species_list[0],
            Species(source="GBIF", id=1, scientific_name="Parkia"),
        )
        self.assertEqual(gbif_species_list[0].rank, "GENUS")

    @responses.activate
    def test_fetch_data_timeout(self):
        responses.add(
            responses.GET,
            "http://api.gbif.org/v1/species/search?q=Parkia+speciosa&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
            body=Timeout(),
            status=502,
        )
        responses.add(
            responses.GET,
            "http://api.gbif.org/v1/species/search?q=Parkia&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
            body=Timeout(),
            status=502,
        )
        gbif_species_list = GbifService().fetch_data(
            "Parkia speciosa", self.description
        )
        self.assertEqual(gbif_species_list, [])


if __name__ == "__main__":
    test_main()
