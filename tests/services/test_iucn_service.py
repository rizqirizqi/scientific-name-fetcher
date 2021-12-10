import responses
from unittest import TestCase, main as test_main
from requests import Timeout
from unittest.mock import patch
from scifetcher.services.iucn_service import IucnService


@patch.dict(
    "scifetcher.config.ENV_CONFIG",
    {"AUTO_SEARCH_SIMILAR_SPECIES": "True", "IUCN_API_TOKEN": "1UCN_4P1_T0K3N"},
    clear=True,
)
class TestIucnService(TestCase):

    maxDiff = None

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
        self.assertDictEqual(
            iucn_species_list[0].to_dict(),
            {
                "Accepted Name": "Wrightia pubescens R. Br.",
                "Authorship": "R. Br.",
                "Canonical Name": "Wrightia pubescens",
                "Class": "MAGNOLIOPSIDA",
                "Confidence": "NA",
                "Family": "APOCYNACEAE",
                "Genus": "Wrightia",
                "Kingdom": "PLANTAE",
                "MatchType": "NA",
                "Order": "GENTIANALES",
                "Phylum": "TRACHEOPHYTA",
                "Rank": "SPECIES",
                "Scientific Name": "Wrightia pubescens R. Br.",
                "Search URL": "NA",
                "Source": "IUCN",
                "Source Key": 62544,
                "Species": "Wrightia pubescens",
                "Status": "NA",
                "Threat Status": "LC",
                "URL": "https://www.iucnredlist.org/species/145672353/145672355",
            },
        )
        self.assertDictEqual(
            iucn_species_list[1].to_dict(),
            {
                "Accepted Name": "Wrightia novobritannica (Ngan) D.J.Middleton",
                "Authorship": "(Ngan) D.J.Middleton",
                "Canonical Name": "Wrightia novobritannica",
                "Class": "MAGNOLIOPSIDA",
                "Confidence": "NA",
                "Family": "APOCYNACEAE",
                "Genus": "Wrightia",
                "Kingdom": "PLANTAE",
                "MatchType": "NA",
                "Order": "GENTIANALES",
                "Phylum": "TRACHEOPHYTA",
                "Rank": "SPECIES",
                "Scientific Name": "Wrightia pubescens R.Br.",
                "Search URL": "NA",
                "Source": "IUCN",
                "Source Key": 143755417,
                "Species": "Wrightia novobritannica",
                "Status": "NA",
                "Threat Status": "DD",
                "URL": "https://www.iucnredlist.org/species/145672353/145672356",
            },
        )
        self.assertDictEqual(
            iucn_species_list[2].to_dict(),
            {
                "Accepted Name": "Wrightia candollei S.Vidal",
                "Authorship": "S.Vidal",
                "Canonical Name": "Wrightia candollei",
                "Class": "MAGNOLIOPSIDA",
                "Confidence": "NA",
                "Family": "APOCYNACEAE",
                "Genus": "Wrightia",
                "Kingdom": "PLANTAE",
                "MatchType": "NA",
                "Order": "GENTIANALES",
                "Phylum": "TRACHEOPHYTA",
                "Rank": "SPECIES",
                "Scientific Name": "Wrightia pubescens Roth",
                "Search URL": "NA",
                "Source": "IUCN",
                "Source Key": 154610271,
                "Species": "Wrightia candollei",
                "Status": "NA",
                "Threat Status": "NT",
                "URL": "https://www.iucnredlist.org/species/145672353/145672357",
            },
        )

    @responses.activate
    def test_fetch_data_search_synonym_success(self):
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/synonym/Cassia%20alata?token=1UCN_4P1_T0K3N",
            json={
                "name": "Cassia alata",
                "count": 1,
                "result": [
                    {
                        "accepted_id": 144263375,
                        "accepted_name": "Senna alata",
                        "authority": "(L.) Roxb.",
                        "synonym": "Cassia alata",
                        "syn_authority": "L.",
                    }
                ],
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/Cassia%20alata?token=1UCN_4P1_T0K3N",
            json={"value": "0", "species": "Cassia alata"},
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/weblink/Cassia%20alata",
            json={
                "rlurl": "https://www.iucnredlist.org/species/144263375/149048081",
                "species": "Cassia alata",
            },
            status=200,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/Senna%20alata?token=1UCN_4P1_T0K3N",
            json={
                "name": "Senna alata",
                "result": [
                    {
                        "taxonid": 144263375,
                        "scientific_name": "Senna alata",
                        "kingdom": "PLANTAE",
                        "phylum": "TRACHEOPHYTA",
                        "class": "MAGNOLIOPSIDA",
                        "order": "FABALES",
                        "family": "FABACEAE",
                        "genus": "Senna",
                        "main_common_name": None,
                        "authority": "(L.) Roxb.",
                        "published_year": 2019,
                        "assessment_date": "2018-06-12",
                        "category": "LC",
                        "criteria": None,
                        "population_trend": "Stable",
                        "marine_system": False,
                        "freshwater_system": False,
                        "terrestrial_system": True,
                        "assessor": "Botanic Gardens Conservation International (BGCI) & IUCN SSC Global Tree Specialist Group",
                        "reviewer": "Oldfield, S.",
                        "aoo_km2": "1188.00",
                        "eoo_km2": "11649465.11",
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
            "https://apiv3.iucnredlist.org/api/v3/weblink/Senna%20alata",
            json={
                "rlurl": "https://www.iucnredlist.org/species/144263375/149048081",
                "species": "Senna alata",
            },
            status=200,
        )
        iucn_species_list = IucnService().fetch_data("Cassia alata", None)
        self.assertEqual(len(iucn_species_list), 1)
        self.assertDictEqual(
            iucn_species_list[0].to_dict(),
            {
                "Accepted Name": "Senna alata (L.) Roxb.",
                "Authorship": "(L.) Roxb.",
                "Canonical Name": "Senna alata",
                "Class": "MAGNOLIOPSIDA",
                "Confidence": "NA",
                "Family": "FABACEAE",
                "Genus": "Senna",
                "Kingdom": "PLANTAE",
                "MatchType": "NA",
                "Order": "FABALES",
                "Phylum": "TRACHEOPHYTA",
                "Rank": "SPECIES",
                "Scientific Name": "Cassia alata L.",
                "Search URL": "NA",
                "Source": "IUCN",
                "Source Key": 144263375,
                "Species": "Senna alata",
                "Status": "NA",
                "Threat Status": "LC",
                "URL": "https://www.iucnredlist.org/species/144263375/149048081",
            },
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

    @responses.activate
    def test_fetch_data_timeout(self):
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/synonym/Wrightia%20pubescens?token=1UCN_4P1_T0K3N",
            body=Timeout(),
            status=502,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/species/Wrightia%20pubescens?token=1UCN_4P1_T0K3N",
            body=Timeout(),
            status=502,
        )
        responses.add(
            responses.GET,
            "https://apiv3.iucnredlist.org/api/v3/weblink/Wrightia%20pubescens",
            body=Timeout(),
            status=502,
        )
        gbif_species_list = IucnService().fetch_data("Wrightia pubescens", None)
        self.assertEqual(gbif_species_list, [])


if __name__ == "__main__":
    test_main()
