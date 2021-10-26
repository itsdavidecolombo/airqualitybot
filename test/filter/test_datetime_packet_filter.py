#################################################
#
# @Author: davidecolombo
# @Date: mar, 26-10-2021, 12:57
# @Description: unit test script
#
#################################################

import unittest
from airquality.filter.datetime_packet_filter import DatetimePacketFilterFactory
from airquality.constants.shared_constants import ATMOTUBE_TIME_PARAM


class TestDatetimeFilter(unittest.TestCase):


    def setUp(self) -> None:
        self.factory = DatetimePacketFilterFactory()


    def test_successfully_filter_atmotube_packets(self):
        test_packets = [{ATMOTUBE_TIME_PARAM: "2021-10-11T09:44:00.000Z"},
                        {ATMOTUBE_TIME_PARAM: "2021-10-11T09:45:00.000Z"},
                        {ATMOTUBE_TIME_PARAM: "2021-10-11T09:46:00.000Z"}]
        test_sqltimestamp = "2021-10-11 09:45:00"
        expected_output = [{ATMOTUBE_TIME_PARAM: "2021-10-11T09:46:00.000Z"}]
        filter_ = self.factory.create_datetime_filter(bot_personality = "atmotube")
        actual_output = filter_.filter_packets(packets = test_packets, sqltimestamp = test_sqltimestamp)
        self.assertEqual(actual_output, expected_output)




if __name__ == '__main__':
    unittest.main()