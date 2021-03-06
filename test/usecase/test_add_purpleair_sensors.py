######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 20:21
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import test._test_utils as tutils
from datetime import datetime
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.usecase.purpleair import Purpleair


def _test_timezone():
    return tutils.get_tzinfo_from_coordinates(latitude=45, longitude=9)


def _mocked_datetime_utcfromtimestamp() -> MagicMock:
    mocked_utcfrom = MagicMock()
    mocked_utcfrom.return_value = datetime(2018, 9, 29, 21, 10, 23, tzinfo=_test_timezone())
    return mocked_utcfrom


def _mocked_datetime_now() -> MagicMock:
    mocked_now = MagicMock()
    mocked_now.return_value = datetime(2021, 12, 29, 19, 33, tzinfo=_test_timezone())
    return mocked_now


def _setup_mocked_json_response() -> MagicMock:
    mocked_resp = MagicMock()
    mocked_resp.status_code = 200
    mocked_resp.json.return_value = tutils.get_json_response_from_file(filename='purpleair_response.json')
    return mocked_resp


def _expected_apiparam_record() -> str:
    ts = '2018-09-29 23:10:23+02:00'
    return f"(1,'key1a3','119','1A','{ts}')," \
           f"(1,'key1b3','120','1B','{ts}')," \
           f"(1,'key2a3','121','2A','{ts}')," \
           f"(1,'key2b3','122','2B','{ts}')"


def _expected_sensor_record() -> str:
    return "(1,'Purpleair/Thingspeak','n3 (3)')"


# def _expected_sensor_at_location_record() -> str:
#     return "(1, '2021-12-29 19:33:00+01:00', ST_GeomFromText('POINT(9.12 45.24)', 4326))"


def _expected_insert_sensors_query():
    return f"INSERT INTO level0_raw.sensor VALUES {_expected_sensor_record()};" \
            "INSERT INTO level0_raw.sensor_api_param (sensor_id, ch_key, ch_id, ch_name, last_acquisition) VALUES " \
            f"{_expected_apiparam_record()};"


def _test_existing_sensor_names():
    return {'n1 (1)', 'n2 (2)'}


def _test_max_sensor_id_plus_one() -> int:
    return 1


def _setup_mocked_database_gway() -> MagicMock:
    mocked_gateway = MagicMock()
    mocked_gateway.query_max_sensor_id_plus_one.return_value = _test_max_sensor_id_plus_one()
    mocked_gateway.query_sensor_names_of_type.return_value = _test_existing_sensor_names()
    mocked_gateway.execute = MagicMock()
    return mocked_gateway


class AddPurpleairFixedSensorsIntegrationTest(TestCase):
    """
    A class that defines the integration tests for asserting the right behavior of *AddPurpleairFixedSensors* usecase.
    """

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._mocked_database_gway = _setup_mocked_database_gway()
        self._usecase = Purpleair(database_gway=self._mocked_database_gway)

# =========== TEST METHODS
    @patch('airquality.environment.os')
    @patch('airquality.extra.timest.datetime')
    @patch('airquality.extra.url.requests.get')
    def test_add_fixed_sensors_usecase(self, mocked_get, mocked_datetime, mocked_os):
        mocked_os.environ = {'purpleair_url': 'fake_url'}
        mocked_get.return_value = _setup_mocked_json_response()
        mocked_datetime.now = _mocked_datetime_now()
        mocked_datetime.utcfromtimestamp = _mocked_datetime_utcfromtimestamp()
        self._usecase.execute()
        self._assert_responses()
        self._assert_usecase_properties()

# =========== SUPPORT METHODS
    def _assert_responses(self):
        query = self._mocked_database_gway.execute.call_args[0][0]
        self.assertEqual(
            query,
            _expected_insert_sensors_query()
        )

    def _assert_usecase_properties(self,):
        self.assertEqual(self._usecase._start_sensor_id, 1)
        self.assertEqual(len(self._usecase._database_sensor_names), 2)
        self.assertIn('n1 (1)', self._usecase._database_sensor_names)
        self.assertIn('n2 (2)', self._usecase._database_sensor_names)


if __name__ == '__main__':
    main()
