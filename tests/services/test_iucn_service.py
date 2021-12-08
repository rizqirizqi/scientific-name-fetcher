import responses
from unittest import TestCase, main as test_main
from requests import Timeout
from unittest.mock import patch
from scifetcher.config import ENV_CONFIG
from scifetcher.models.species import Species
from scifetcher.services.iucn_service import IucnService


@patch.dict(
    "scifetcher.config.ENV_CONFIG",
    {"AUTO_SEARCH_SIMILAR_SPECIES": "True", "IUCN_API_TOKEN": "1UCN_4P1_T0K3N"},
    clear=True,
)
class TestIucnService(TestCase):

    description = "Parkia speciasa (the bitter bean, twisted cluster bean, or stink bean) is a plant of the genus Parkia in the family Fabaceae.  It bears long, flat edible beans with bright green seeds the size and shape of plump almonds which have a rather peculiar smell, similar to, but stronger than that of the shiitake mushroom, due to sulfur-containing compounds also found in shiitake, truffles and cabbage."

    @responses.activate
    def test_fetch_data_search_success(self):
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/synonym/Wrightia%20pubescens?token=1UCN_4P1_T0K3N",
            json={
                "name": "Wrightia pubescens",
                "count": 2,
                "result": [
                    {
                        "accepted_id": 143755417,
                        "accepted_name": "Wrightia novobritannica",
                        "authority": "(Ngan) D.J.Middleton",
                        "synonym": "Wrightia pubescens",
                        "syn_authority": "R.Br.",
                    },
                    {
                        "accepted_id": 154610271,
                        "accepted_name": "Wrightia candollei",
                        "authority": "S.Vidal",
                        "synonym": "Wrightia pubescens",
                        "syn_authority": "Roth",
                    },
                ],
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/Wrightia%20pubescens?token=1UCN_4P1_T0K3N",
            json={
                "name": "Wrightia pubescens",
                "result": [
                    {
                        "taxonid": 62544,
                        "scientific_name": "Wrightia pubescens",
                        "kingdom": "PLANTAE",
                        "phylum": "TRACHEOPHYTA",
                        "class": "MAGNOLIOPSIDA",
                        "order": "GENTIANALES",
                        "family": "APOCYNACEAE",
                        "genus": "Wrightia",
                        "main_common_name": None,
                        "authority": "R. Br.",
                        "published_year": 2019,
                        "assessment_date": "2019-01-02",
                        "category": "LC",
                        "criteria": None,
                        "population_trend": "Stable",
                        "marine_system": False,
                        "freshwater_system": False,
                        "terrestrial_system": True,
                        "assessor": "Barstow, M.",
                        "reviewer": "Jimbo, T.",
                        "aoo_km2": None,
                        "eoo_km2": None,
                        "elevation_upper": 300,
                        "elevation_lower": None,
                        "depth_upper": None,
                        "depth_lower": None,
                        "errata_flag": None,
                        "errata_reason": None,
                        "amended_flag": None,
                        "amended_reason": None,
                    }
                ],
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/Wrightia%20novobritannica?token=1UCN_4P1_T0K3N",
            json={
                "name": "Wrightia novobritannica",
                "result": [
                    {
                        "taxonid": 143755417,
                        "scientific_name": "Wrightia novobritannica",
                        "kingdom": "PLANTAE",
                        "phylum": "TRACHEOPHYTA",
                        "class": "MAGNOLIOPSIDA",
                        "order": "GENTIANALES",
                        "family": "APOCYNACEAE",
                        "genus": "Wrightia",
                        "main_common_name": None,
                        "authority": "(Ngan) D.J.Middleton",
                        "published_year": 2020,
                        "assessment_date": "2020-01-20",
                        "category": "DD",
                        "criteria": None,
                        "population_trend": "Unknown",
                        "marine_system": False,
                        "freshwater_system": False,
                        "terrestrial_system": True,
                        "assessor": "IUCN SSC Global Tree Specialist Group",
                        "reviewer": "Jimbo, T.",
                        "aoo_km2": None,
                        "eoo_km2": None,
                        "elevation_upper": None,
                        "elevation_lower": None,
                        "depth_upper": None,
                        "depth_lower": None,
                        "errata_flag": None,
                        "errata_reason": None,
                        "amended_flag": None,
                        "amended_reason": None,
                    }
                ],
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/Wrightia%20candollei?token=1UCN_4P1_T0K3N",
            json={
                "name": "Wrightia candollei",
                "result": [
                    {
                        "taxonid": 154610271,
                        "scientific_name": "Wrightia candollei",
                        "kingdom": "PLANTAE",
                        "phylum": "TRACHEOPHYTA",
                        "class": "MAGNOLIOPSIDA",
                        "order": "GENTIANALES",
                        "family": "APOCYNACEAE",
                        "genus": "Wrightia",
                        "main_common_name": None,
                        "authority": "S.Vidal",
                        "published_year": 2020,
                        "assessment_date": "2020-01-09",
                        "category": "NT",
                        "criteria": None,
                        "population_trend": "Decreasing",
                        "marine_system": False,
                        "freshwater_system": False,
                        "terrestrial_system": True,
                        "assessor": "Energy Development Corporation (EDC) ",
                        "reviewer": "Tobias, A.B., Malabrigo, P., Umali, A., Eduarte, G., Magbuo, J.M., Divina, A. & Barstow, M.",
                        "aoo_km2": "92",
                        "eoo_km2": "363000",
                        "elevation_upper": 500,
                        "elevation_lower": 100,
                        "depth_upper": None,
                        "depth_lower": None,
                        "errata_flag": None,
                        "errata_reason": None,
                        "amended_flag": None,
                        "amended_reason": None,
                    }
                ],
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/weblink/Wrightia%20pubescens",
            json={
                "rlurl": "https://www.iucnredlist.org/species/145672353/145672355",
                "species": "Wrightia pubescens",
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/weblink/Wrightia%20novobritannica",
            json={
                "rlurl": "https://www.iucnredlist.org/species/145672353/145672356",
                "species": "Wrightia novobritannica",
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/weblink/Wrightia%20candollei",
            json={
                "rlurl": "https://www.iucnredlist.org/species/145672353/145672357",
                "species": "Wrightia candollei",
            },
            status=200,
        )
        iucn_species_list = IucnService().fetch_data("Wrightia pubescens", None)
        self.assertEqual(len(iucn_species_list), 3)
        self.assertEqual(
            iucn_species_list,
            [
                Species(source="IUCN", id=62544, scientific_name="Wrightia pubescens"),
                Species(
                    source="IUCN",
                    id=143755417,
                    scientific_name="Wrightia novobritannica",
                ),
                Species(
                    source="IUCN", id=154610271, scientific_name="Wrightia candollei"
                ),
            ],
        )

    @responses.activate
    def test_fetch_data_search_notfound(self):
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/synonym/Grewia%20multiflora?token=1UCN_4P1_T0K3N",
            json={"name": "Grewia multiflora", "count": 0, "result": []},
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/Grewia%20multiflora?token=1UCN_4P1_T0K3N",
            json={"name": "Grewia multiflora", "result": []},
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/weblink/Grewia%20multiflora",
            json={
                "value": "0",
                "species": "Grewia multiflora",
                "message": "species name not found!",
            },
            status=200,
        )
        iucn_species_list = IucnService().fetch_data("Grewia multiflora", None)
        self.assertEqual(len(iucn_species_list), 0)

    # @responses.activate
    # def test_fetch_data_success_similar_name(self):
    #     responses.add(
    #         responses.GET,
    #         "http://api.gbif.org/v1/species/search?q=Parkia+speciosa&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
    #         json={"count": 0,},
    #         status=200,
    #     )
    #     responses.add(
    #         responses.GET,
    #         "http://api.gbif.org/v1/species/search?q=Parkia+speciasa&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
    #         json={
    #             "count": 1,
    #             "results": [
    #                 {
    #                     "key": 1,
    #                     "constituentKey": 1,
    #                     "taxonomicStatus": "ACCEPTED",
    #                     "rank": "SPECIES",
    #                     "scientificName": "Parkia speciasa Asa.",
    #                     "canonicalName": "Parkia speciasa",
    #                     "authorship": "Asa.",
    #                     "kingdom": "Viridiplantae",
    #                     "phylum": "Streptophyta",
    #                     "class": "Magnoliopsida",
    #                     "order": "Fabales",
    #                     "family": "Fabaceae",
    #                     "genus": "Parkia",
    #                     "species": "Parkia speciasa",
    #                 },
    #             ],
    #         },
    #         status=200,
    #     )
    #     gbif_species_list = IucnService().fetch_data(
    #         "Parkia speciosa", self.description
    #     )
    #     self.assertEqual(len(gbif_species_list), 1)
    #     self.assertEqual(
    #         gbif_species_list[0],
    #         Species(source="GBIF", id=1, scientific_name="Parkia speciasa Asa."),
    #     )

    # @responses.activate
    # def test_fetch_data_success_genus(self):
    #     responses.add(
    #         responses.GET,
    #         "http://api.gbif.org/v1/species/search?q=Parkia+speciosa&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
    #         json={"count": 0,},
    #         status=200,
    #     )
    #     responses.add(
    #         responses.GET,
    #         "http://api.gbif.org/v1/species/search?q=Parkia&limit=100&locale=en&advanced=false&facet=origin&issue.facetLimit=100&name_type.facetLimit=100&rank.facetLimit=100&status.facetLimit=100&facetMultiselect=true",
    #         json={
    #             "count": 1,
    #             "results": [
    #                 {
    #                     "key": 1,
    #                     "constituentKey": 1,
    #                     "taxonomicStatus": "ACCEPTED",
    #                     "rank": "GENUS",
    #                     "scientificName": "Parkia",
    #                     "canonicalName": "Parkia",
    #                     "kingdom": "Viridiplantae",
    #                     "phylum": "Streptophyta",
    #                     "class": "Magnoliopsida",
    #                     "order": "Fabales",
    #                     "family": "Fabaceae",
    #                     "genus": "Parkia",
    #                 },
    #             ],
    #         },
    #         status=200,
    #     )
    #     gbif_species_list = IucnService().fetch_data("Parkia speciosa", None)
    #     self.assertEqual(len(gbif_species_list), 1)
    #     self.assertEqual(
    #         gbif_species_list[0],
    #         Species(source="GBIF", id=1, scientific_name="Parkia"),
    #     )
    #     self.assertEqual(gbif_species_list[0].rank, "GENUS")

    # @responses.activate
    # def test_fetch_data_timeout(self):
    #     responses.add(
    #         responses.GET,
    #         "https://apiv3.iucnredlist.org/api/v3/species/synonym/Wrightia%20pubescens?token=1UCN_4P1_T0K3N",
    #         body=Timeout(),
    #         status=502,
    #     )
    #     responses.add(
    #         responses.GET,
    #         "https://apiv3.iucnredlist.org/api/v3/species/Wrightia%20pubescens?token=1UCN_4P1_T0K3N",
    #         body=Timeout(),
    #         status=502,
    #     )
    #     gbif_species_list = IucnService().fetch_data(
    #         "Wrightia pubescens", self.description
    #     )
    #     self.assertEqual(gbif_species_list, [])


if __name__ == "__main__":
    test_main()
