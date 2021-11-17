######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 13/11/21 15:56
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import unittest
from typing import Dict, Any
import airquality.adapter.api2db.measure as adapt
import airquality.database.operation.select.type as sel_type


############################## ATMOTUBE MOCK #############################
class AtmotubeTypeSelectWrapperMock(sel_type.TypeSelectWrapper):

    def get_max_record_id(self):
        return 99

    def get_measure_param(self) -> Dict[str, Any]:
        return {'voc': 1, 'pm1': 2, 'pm25': 3, 'pm10': 4, 't': 5, 'h': 6, 'p': 7}


############################## THINGSPEAK MOCK #############################
class ThingspeakTypeSelectWrapperMock(sel_type.TypeSelectWrapper):

    def get_max_record_id(self):
        return 99

    def get_measure_param(self) -> Dict[str, Any]:
        return {'f1': 9, 'f2': 10}


############################## TEST CLASS #############################
class TestMeasureReshaper(unittest.TestCase):

    def setUp(self) -> None:
        self.atmotube_adapter = adapt.AtmotubeMeasureAdapter(
            type_wrapper=AtmotubeTypeSelectWrapperMock(conn=None, query_builder=None, sensor_type=None)
        )
        self.thingspeak_adapter = adapt.ThingspeakMeasureAdapter(
            type_wrapper=ThingspeakTypeSelectWrapperMock(conn=None, query_builder=None, sensor_type=None)
        )

    ############################## TEST ATMOTUBE MEASURE ADAPTER #############################
    def test_successfully_reshape_atmotube_measurements(self):
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'time': '2021-10-11T01:33:44.000Z'}
        expected_output = {'record_id': 99, 'timestamp': '2021-10-11T01:33:44.000Z',
                           'param_id': [1, 2, 3, 4, 5, 6, 7],
                           'param_value': ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7']}
        actual_output = self.atmotube_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

        # Test when 'coords' are not missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                       'p': 'val7', 'time': '2021-10-11T01:33:44.000Z', 'coords': {'lat': 'lat_val', 'lon': 'lon_val'}}
        expected_output = {'record_id': 100, 'lat': 'lat_val', 'lng': 'lon_val', 'timestamp': '2021-10-11T01:33:44.000Z',
                           'param_id': [1, 2, 3, 4, 5, 6, 7],
                           'param_value': ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7']}
        actual_output = self.atmotube_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_none_value_when_field_is_missing(self):
        # Test output when 't', 'h' and 'p' are missing
        test_packet = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 'time': '2021-10-11T01:33:44.000Z'}
        expected_output = {'record_id': 99, 'timestamp': '2021-10-11T01:33:44.000Z',
                           'param_id': [1, 2, 3, 4, 5, 6, 7],
                           'param_value': ['val1', 'val2', 'val3', 'val4', None, None, None]}
        actual_output = self.atmotube_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_param_is_missing(self):
        # Test when 'coords' are not missing
        test_bad_coords = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                           'p': 'val7', 'coords': {}}
        with self.assertRaises(SystemExit):
            self.atmotube_adapter.reshape(test_bad_coords)

        test_missing_time = {'voc': 'val1', 'pm1': 'val2', 'pm25': 'val3', 'pm10': 'val4', 't': 'val5', 'h': 'val6',
                             'p': 'val7'}
        with self.assertRaises(SystemExit):
            self.atmotube_adapter.reshape(test_missing_time)

    ############################## TEST THINGSPEAK MEASURE ADAPTER #############################
    def test_successfully_adapt_thingspeak_data(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'name': 'f1', 'value': 'val1'},
                                  {'name': 'f2', 'value': 'val2'}]}

        expected_output = {'record_id': 99, 'timestamp': '2021-10-11T01:33:44Z',
                           'param_id': [9, 10],
                           'param_value': ['val1', 'val2']}
        actual_output = self.thingspeak_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_none_value_when_param_is_null(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'name': 'f1', 'value': None},
                                  {'name': 'f2', 'value': 'val2'}]}

        expected_output = {'record_id': 99, 'timestamp': '2021-10-11T01:33:44Z',
                           'param_id': [9, 10],
                           'param_value': [None, 'val2']}
        actual_output = self.thingspeak_adapter.reshape(test_packet)
        self.assertEqual(actual_output, expected_output)

    def test_system_exit_when_key_error_is_raised(self):
        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'name': 'f1', 'bad_key': 'val1'},
                                  {'name': 'f2', 'bad_key': 'val2'}]}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_packet)

        test_packet = {'created_at': '2021-10-11T01:33:44Z',
                       'fields': [{'bad_key': 'f1', 'value': 'val1'},
                                  {'bad_key': 'f2', 'value': 'val2'}]}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_packet)

        test_packet = {'created_at': '2021-10-11T01:33:44Z'}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_packet)

        test_packet = {'fields': [{'name': 'f1', 'value': None},
                                  {'name': 'f2', 'value': 'val2'}]}
        with self.assertRaises(SystemExit):
            self.thingspeak_adapter.reshape(test_packet)


if __name__ == '__main__':
    unittest.main()