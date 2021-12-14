######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 10:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import api as urltype


class TestBaseURL(unittest.TestCase):

    def setUp(self) -> None:
        self.test_url_template = "some_address?api_key=some_key&fields=f1,f2&opt1=1&opt2=abc"

    def test_successfully_build_purpleair_url(self):
        builder = urltype.PurpleairURLBuilder(url_template=self.test_url_template)
        expected = self.test_url_template
        actual = builder.execute()
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()