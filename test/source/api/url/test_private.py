######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 10:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import api as urltype


class TestDynamicURL(unittest.TestCase):

    def setUp(self) -> None:
        self.test_atm_url_template = "some_address?api_key={api_key}&mac={mac}&order=asc&format={fmt}"
        self.test_atm_url_template_with_options = "some_address?api_key={api_key}&mac={mac}&order=asc&format={fmt}&opt1=v1&opt2=33"
        self.test_thnk_url_template = "some_address/{channel_id}/feeds.{fmt}?api_key={api_key}"
        self.test_thnk_url_template_with_options = "some_address/{channel_id}/feeds.{fmt}?api_key={api_key}&opt1=v1&opt2=33"

    def test_successfully_build_atmotube_url(self):
        builder = urltype.AtmotubeURLBuilder(self.test_atm_url_template, api_key="k", ident="m", fmt="fmt")
        actual = builder.execute()
        expected = "some_address?api_key=k&mac=m&order=asc&format=fmt"
        self.assertEqual(actual, expected)

    def test_successfully_build_atmotube_url_with_options(self):
        builder = urltype.AtmotubeURLBuilder(self.test_atm_url_template_with_options, api_key="k", ident="m", fmt="fmt")
        actual = builder.execute()
        expected = "some_address?api_key=k&mac=m&order=asc&format=fmt&opt1=v1&opt2=33"
        self.assertEqual(actual, expected)

    def test_successfully_build_thingspeak_url(self):
        builder = urltype.ThingspeakURLBuilder(self.test_thnk_url_template, api_key="k", ident="id", fmt="fmt")
        expected = "some_address/id/feeds.fmt?api_key=k"
        actual = builder.execute()
        self.assertEqual(actual, expected)

    def test_successfully_build_thingspeak_url_with_options(self):
        builder = urltype.ThingspeakURLBuilder(self.test_thnk_url_template_with_options, api_key="k", ident="id", fmt="fmt")
        actual = builder.execute()
        expected = "some_address/id/feeds.fmt?api_key=k&opt1=v1&opt2=33"
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()