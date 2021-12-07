######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:47
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from unittest.mock import Mock
import airquality.filter.geofilt as flt
import airquality.types.apiresp.inforesp as resp
import airquality.types.geolocation as geotype
import airquality.types.postgis as pgis
import airquality.types.lookup.lookup as lookuptype


class TestGeoFilter(unittest.TestCase):

    def setUp(self) -> None:
        geolocation1 = geotype.Geolocation(timestamp=None, geometry=pgis.PostgisPoint(lat="45", lng="9"))
        geolocation2 = geotype.Geolocation(timestamp=None, geometry=pgis.PostgisPoint(lat="46", lng="8"))
        geolocation3 = geotype.Geolocation(timestamp=None, geometry=pgis.PostgisPoint(lat="45.5", lng="8.5"))

        self.test_responses = [
            resp.SensorInfoResponse(sensor_name="n1", sensor_type="t1", channels=[], geolocation=geolocation1),
            resp.SensorInfoResponse(sensor_name="n2", sensor_type="t1", channels=[], geolocation=geolocation2),
            resp.SensorInfoResponse(sensor_name="n3", sensor_type="t1", channels=[], geolocation=geolocation3)
        ]

    def test_empty_list_when_active_locations_are_the_same(self):
        mocked_repo = Mock()
        mocked_repo.lookup.return_value = [lookuptype.SensorGeoLookup(
            sensor_name="n1", geometry=pgis.PostgisPoint(lat="45", lng="9")
        )]
        resp_filter = flt.GeoFilter(repo=mocked_repo)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 0)

    def test_successfully_filter_responses(self):
        mocked_repo = Mock()
        mocked_repo.lookup.return_value = [lookuptype.SensorGeoLookup(
            sensor_name="n1", geometry=pgis.PostgisPoint(lat="44", lng="10")
        )]
        resp_filter = flt.GeoFilter(repo=mocked_repo)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].sensor_name, "n1")

    def test_empty_list_when_no_active_locations_is_fetched(self):
        mocked_repo = Mock()
        mocked_repo.lookup.return_value = []
        resp_filter = flt.GeoFilter(repo=mocked_repo)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 0)


if __name__ == '__main__':
    unittest.main()
