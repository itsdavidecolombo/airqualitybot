# ======================================
# @author:  Davide Colombo
# @date:    2022-02-1, mar, 10:15
# ======================================
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock, patch
from airquality.datamodel.fromdb import SensorLocationDM
from airquality.usecase.purp_update import PurpUpdate


def _test_queried_locations():
    return SensorLocationDM(
        sensor_id=12,
        longitude=9.44,
        latitude=45.99
    )


def _mocked_database_gateway():
    mocked_dg = MagicMock()
    mocked_dg.execute = MagicMock()
    mocked_dg.query_purpleair_sensor_location.return_value = _test_queried_locations()
    return mocked_dg


def _setup_mocked_json_response() -> MagicMock:
    mocked_resp = MagicMock()
    mocked_resp.status_code = 200
    mocked_resp.json.return_value = tutils.get_json_response_from_file(filename='purpleair_response.json')
    return mocked_resp


def _test_tzinfo():
    return tutils.get_tzinfo_from_timezone_name(tzname='Europe/Rome')


def _mocked_now():
    return datetime(2022, 1, 22, 10, 37, tzinfo=_test_tzinfo())


def _expected_update_insert_query():
    ts = '2022-01-22 10:37:00+01:00'
    geom = "ST_GeomFromText('POINT(13.2222 78.9999)', 4326)"
    return f"UPDATE level0_raw.sensor_at_location SET valid_to = '{ts}' WHERE sensor_id = 12 AND valid_to IS NULL;" \
           f"INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) VALUES (12, '{ts}', {geom});"


class TestUpdatePurpleairLocationsUsecase(TestCase):

    @patch('airquality.extra.timest.datetime')
    @patch('airquality.extra.url.requests.get')
    def test_update_purpleair_locations(self, mocked_get, mocked_datetime):
        mocked_datetime.now.return_value = _mocked_now()
        mocked_get.return_value = _setup_mocked_json_response()
        mocked_database_gway = _mocked_database_gateway()
        usecase = PurpUpdate(database_gway=mocked_database_gway)
        usecase.execute()

        query = mocked_database_gway.execute.call_args[1]['query']
        self.assertEqual(
            query,
            _expected_update_insert_query()
        )

        self.assertEqual(
            mocked_database_gway.execute.call_count,
            3
        )


if __name__ == '__main__':
    main()
