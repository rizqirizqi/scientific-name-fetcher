from unittest import TestCase, main as test_main
from requests import Timeout
from scifetcher.services.wiki_service import WikiService
import responses


class TestWikiService(TestCase):

    extract = "Parkia speciosa (the bitter bean, twisted cluster bean, or stink bean) is a plant of the genus Parkia in the family Fabaceae.  It bears long, flat edible beans with bright green seeds the size and shape of plump almonds which have a rather peculiar smell, similar to, but stronger than that of the shiitake mushroom, due to sulfur-containing compounds also found in shiitake, truffles and cabbage."

    @responses.activate
    def test_fetch_data_success_fetch_description(self):
        responses.add(
            responses.GET,
            "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exlimit=max&format=json&exsentences=2&origin=%2A&exintro=true&explaintext=true&generator=search&gsrsearch=Parkia+speciosa",
            json={
                "batchcomplete": "",
                "query": {
                    "pages": {
                        "12345": {
                            "index": 1,
                            "title": "Parkia speciosa",
                            "extract": self.extract,
                        }
                    }
                },
                "limits": {"extracts": 20},
            },
            status=200,
        )
        description = WikiService().fetch_data("Parkia speciosa")
        self.assertEqual(description, self.extract)

    @responses.activate
    def test_fetch_data_success_fetch_recommended_keyword(self):
        responses.add(
            responses.GET,
            "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exlimit=max&format=json&exsentences=2&origin=%2A&exintro=true&explaintext=true&generator=search&gsrsearch=Abarema+clypearia",
            json={"batchcomplete": "", "limits": {"extracts": 20}},
            status=200,
        )
        responses.add(
            responses.GET,
            "https://commons.wikimedia.org/w/api.php?action=opensearch&search=Abarema+clypearia",
            json=["Abarema clypearia", ["Archidendron clypearia"]],
            status=200,
        )
        description = WikiService().fetch_data("Abarema clypearia")
        self.assertEqual(description, "Do you mean: Archidendron clypearia")

    @responses.activate
    def test_fetch_data_timeout(self):
        responses.add(
            responses.GET,
            "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exlimit=max&format=json&exsentences=2&origin=%2A&exintro=true&explaintext=true&generator=search&gsrsearch=Parkia+speciosa",
            body=Timeout(),
            status=200,
        )
        description = WikiService().fetch_data("Parkia speciosa")
        self.assertEqual(description, "Error, please retry.")


if __name__ == "__main__":
    test_main()
