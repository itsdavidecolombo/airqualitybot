######################################################
#
# Author: Davide Colombo
# Date: 27/11/21 17:39
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
import airquality.filter.namefilt as flt
import airquality.types.apiresp.inforesp as resp


class TestNameFilter(unittest.TestCase):

    def setUp(self) -> None:
        self.test_responses = [
            resp.SensorInfoResponse(sensor_name="n1", sensor_type="t1", channels=[], geolocation=None),
            resp.SensorInfoResponse(sensor_name="n2", sensor_type="t1", channels=[], geolocation=None),
            resp.SensorInfoResponse(sensor_name="n3", sensor_type="t1", channels=[], geolocation=None)
        ]

    def test_successfully_filter_names(self):
        test_database_names = ["n2"]
        resp_filter = flt.NameFilter(database_sensor_names=test_database_names)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].sensor_name, "n1")
        self.assertEqual(actual[1].sensor_name, "n3")

    def test_empty_filtered_list(self):
        test_database_names = ["n1", "n2", "n3"]
        resp_filter = flt.NameFilter(database_sensor_names=test_database_names)
        actual = resp_filter.filter(resp2filter=self.test_responses)
        self.assertEqual(len(actual), 0)


if __name__ == '__main__':
    unittest.main()