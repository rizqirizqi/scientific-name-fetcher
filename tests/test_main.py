import sys
from unittest import TestCase, main as test_main
from unittest.mock import patch
from datetime import date
from scifetcher import __main__


class TestMain(TestCase):
    def test_args(self):
        testargs = [
            "scifetcher",
            "-i",
            "my_test_input.txt",
            "-o",
            "my_test_output.txt",
            "--id-col",
            "ID",
        ]
        with patch.object(sys, "argv", testargs):
            inputfile, outputfile, name_column, id_column = __main__.read_args()
            self.assertEqual(inputfile, "my_test_input.txt")
            self.assertEqual(outputfile, "my_test_output.txt")
            self.assertEqual(name_column, "Names")
            self.assertEqual(id_column, "ID")

    @patch("scifetcher.__main__.datetime")
    def test_no_args(self, mock_datetime):
        testargs = ["scifetcher"]
        with patch.object(sys, "argv", testargs):
            mock_datetime.now.return_value = date(2021, 10, 31)
            mock_datetime.side_effect = lambda *args, **kw: date(*args, **kw)
            inputfile, outputfile, _, _ = __main__.read_args()
            self.assertEqual(inputfile, "input.txt")
            self.assertEqual(outputfile, "result.2021-10-31.000000.txt")


if __name__ == "__main__":
    test_main()
