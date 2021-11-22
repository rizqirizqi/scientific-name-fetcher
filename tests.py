import sys
from unittest import TestCase, main as test_main
from unittest.mock import patch
from datetime import date
from requests import Timeout
from requests.exceptions import RequestException
from scifetcher.apiclients.wiki_api import WikiApi
from scifetcher import __main__


class Tests(TestCase):
    def test_args(self):
        testargs = ["scifetcher", "-i", "my_test_input.txt", "-o", "my_test_output.txt"]
        with patch.object(sys, "argv", testargs):
            inputfile, outputfile, _ = __main__.readArgs()
            self.assertEqual(inputfile, "my_test_input.txt")
            self.assertEqual(outputfile, "my_test_output.txt")

    def test_no_args(self):
        testargs = ["scifetcher"]
        with patch.object(sys, "argv", testargs):
            with patch("scifetcher.__main__.datetime") as mock_datetime:
                mock_datetime.now.return_value = date(2021, 10, 31)
                mock_datetime.side_effect = lambda *args, **kw: date(*args, **kw)
                inputfile, outputfile, _ = __main__.readArgs()
                self.assertEqual(inputfile, "input.txt")
                self.assertEqual(outputfile, "result.2021-10-31.000000.txt")

    @patch("scifetcher.apiclients.wiki_api.requests.get", side_effect=Timeout())
    def test_api_timeout(self, mocked_get):
        with self.assertRaises(RequestException):
            WikiApi("name").get_description()


if __name__ == "__main__":
    test_main()
