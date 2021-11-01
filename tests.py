import sys
from unittest import TestCase, main as test_main
from unittest.mock import patch
import main
from datetime import date

class Tests(TestCase):

    def test_args(self):
        testargs = ["main", "-i", "my_test_input.txt", "-o", "my_test_output.txt"]
        with patch.object(sys, 'argv', testargs):
            inputfile, outputfile = main.readArgs() 
            self.assertEqual(inputfile, "my_test_input.txt")
            self.assertEqual(outputfile, "my_test_output.txt")

    def test_no_args(self):
        testargs = ["main"]
        with patch.object(sys, 'argv', testargs):
            with patch('main.datetime') as mock_datetime:
                mock_datetime.now.return_value = date(2021, 10, 31)
                mock_datetime.side_effect = lambda *args, **kw: date(*args, **kw)
                inputfile, outputfile = main.readArgs() 
                self.assertEqual(inputfile, "input.txt")
                self.assertEqual(outputfile, "result.2021-10-31.00:00:00.txt")

if __name__ == '__main__':
    test_main()
