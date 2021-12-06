import sys
from unittest import TestCase, main as test_main
from unittest.mock import patch
from scifetcher.helpers.string import fuzzy_search


class TestString(TestCase):

    sentence = "Senna alata is an important medicinal tree, as well as an ornamental flowering plant in the subfamily Caesalpinioideae. It also known as emperor's candlesticks, candle bush, candelabra bush, Christmas candles, empress candle plant, ringworm shrub, or candletree."

    def test_fuzzy_search_simple(self):
        result = fuzzy_search(self.sentence, "ornamental")
        self.assertEqual(result, "ornamental")

    def test_fuzzy_search_complex(self):
        result = fuzzy_search(self.sentence, "ornamental flowering plant")
        self.assertEqual(result, "ornamental flowering plant")

    def test_fuzzy_search_perfect(self):
        result = fuzzy_search(self.sentence, "Senna alata")
        self.assertEqual(result, "Senna alata")

    def test_fuzzy_search_typo_genus(self):
        result = fuzzy_search(self.sentence, "Senns alata")
        self.assertEqual(result, "Senna alata")

    def test_fuzzy_search_typo_species(self):
        result = fuzzy_search(self.sentence, "Senna alsta")
        self.assertEqual(result, "Senna alata")

    def test_fuzzy_search_typo_both(self):
        result = fuzzy_search(self.sentence, "Sebba alarw")
        self.assertEqual(result, "Senna alata")

    def test_fuzzy_search_synonym(self):
        result = fuzzy_search("Archidendron clypearia subsp. subcoriaceum is a subspecies of an Archidendron clypearia in the legume family.", "Abarema clypearia")
        self.assertEqual(result, None)


if __name__ == "__main__":
    test_main()
