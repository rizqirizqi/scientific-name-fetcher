from unittest import TestCase, main as test_main
from requests import Timeout
from unittest.mock import MagicMock, patch
from scifetcher.services.powo_service import PowoService


@patch.dict(
    "scifetcher.config.ENV_CONFIG", {"AUTO_SEARCH_SIMILAR_SPECIES": "True"}, clear=True
)
class TestPowoService(TestCase):

    maxDiff = None

    @patch("pykew.powo.search", create=True)
    def test_fetch_data_success(self, powo_search_mock):
        search_result_mock = MagicMock()
        search_result_mock.size.return_value = 3
        search_result_mock.__iter__.return_value = iter(
            [
                {
                    "accepted": True,
                    "author": "L.",
                    "kingdom": "Plantae",
                    "family": "Poaceae",
                    "name": "Poa annua",
                    "rank": "Species",
                    "url": "/taxon/urn:lsid:ipni.org:names:320035-2",
                    "fqId": "urn:lsid:ipni.org:names:320035-2",
                    "images": [
                        {
                            "thumbnail": "//d2seqvvyy3b8p2.cloudfront.net/0df94d250743c4423939be2919a29542.jpg",
                            "fullsize": "//d2seqvvyy3b8p2.cloudfront.net/a74f8c61871d0c6d12b02a1ddcd73a48.jpg",
                            "caption": "Poa annua",
                        },
                    ],
                },
                {
                    "accepted": False,
                    "author": "Schltdl. & Cham.",
                    "kingdom": "Plantae",
                    "family": "Poaceae",
                    "name": "Poa annua",
                    "rank": "Species",
                    "synonymOf": {
                        "accepted": True,
                        "author": "Kunth",
                        "name": "Poa infirma",
                        "url": "/taxon/urn:lsid:ipni.org:names:417256-1",
                        "fqId": "urn:lsid:ipni.org:names:417256-1",
                    },
                    "url": "/taxon/urn:lsid:ipni.org:names:416502-1",
                    "fqId": "urn:lsid:ipni.org:names:416502-1",
                },
                {
                    "accepted": True,
                    "author": "Kunth",
                    "kingdom": "Plantae",
                    "family": "Poaceae",
                    "name": "Poa infirma",
                    "rank": "Species",
                    "url": "/taxon/urn:lsid:ipni.org:names:417256-1",
                    "fqId": "urn:lsid:ipni.org:names:417256-1",
                    "images": [
                        {
                            "thumbnail": "//d2seqvvyy3b8p2.cloudfront.net/c7f0bc221a03a021f41016e979d35fb4.jpg",
                            "fullsize": "//d2seqvvyy3b8p2.cloudfront.net/d1742940eabe2ebab12bc0519e80c4ee.jpg",
                            "caption": "Poa infirma",
                        },
                    ],
                },
            ]
        )
        powo_search_mock.return_value = search_result_mock

        powo_species_list = PowoService().fetch_data("Poa annua")

        self.assertEqual(len(powo_species_list), 3)
        self.assertEqual(
            powo_species_list[0].to_dict(),
            {
                "Accepted Name": "Poa annua L.",
                "Authorship": "L.",
                "Canonical Name": "Poa annua",
                "Class": "NA",
                "Confidence": "NA",
                "Family": "Poaceae",
                "Genus": "Poa",
                "Kingdom": "Plantae",
                "MatchType": "NA",
                "Order": "NA",
                "Phylum": "NA",
                "Rank": "Species",
                "Scientific Name": "Poa annua L.",
                "Search URL": "https://powo.science.kew.org/results?q=Poa%20annua",
                "Source": "POWO",
                "Source Key": "urn:lsid:ipni.org:names:320035-2",
                "Species": "Poa annua",
                "Status": "ACCEPTED",
                "Threat Status": "NA",
                "URL": "https://powo.science.kew.org//taxon/urn:lsid:ipni.org:names:320035-2",
            },
        )
        self.assertEqual(
            powo_species_list[1].to_dict(),
            {
                "Accepted Name": "Poa infirma Kunth",
                "Authorship": "Schltdl. & Cham.",
                "Canonical Name": "Poa annua",
                "Class": "NA",
                "Confidence": "NA",
                "Family": "Poaceae",
                "Genus": "Poa",
                "Kingdom": "Plantae",
                "MatchType": "NA",
                "Order": "NA",
                "Phylum": "NA",
                "Rank": "Species",
                "Scientific Name": "Poa annua Schltdl. & Cham.",
                "Search URL": "https://powo.science.kew.org/results?q=Poa%20annua",
                "Source": "POWO",
                "Source Key": "urn:lsid:ipni.org:names:416502-1",
                "Species": "Poa annua",
                "Status": "SYNONYM",
                "Threat Status": "NA",
                "URL": "https://powo.science.kew.org//taxon/urn:lsid:ipni.org:names:416502-1",
            },
        )
        self.assertEqual(
            powo_species_list[2].to_dict(),
            {
                "Accepted Name": "Poa infirma Kunth",
                "Authorship": "Kunth",
                "Canonical Name": "Poa infirma",
                "Class": "NA",
                "Confidence": "NA",
                "Family": "Poaceae",
                "Genus": "Poa",
                "Kingdom": "Plantae",
                "MatchType": "NA",
                "Order": "NA",
                "Phylum": "NA",
                "Rank": "Species",
                "Scientific Name": "Poa infirma Kunth",
                "Search URL": "https://powo.science.kew.org/results?q=Poa%20annua",
                "Source": "POWO",
                "Source Key": "urn:lsid:ipni.org:names:417256-1",
                "Species": "Poa infirma",
                "Status": "ACCEPTED",
                "Threat Status": "NA",
                "URL": "https://powo.science.kew.org//taxon/urn:lsid:ipni.org:names:417256-1",
            },
        )


if __name__ == "__main__":
    test_main()
