# ======================================
# @author:  Davide Colombo
# @date:    2022-01-24, lun, 09:13
# ======================================
from datetime import datetime
import test._test_utils as tutils
from unittest import TestCase, main
from unittest.mock import MagicMock
from airquality.datamodel.fromdb import SensorApiParamDM
from airquality.datamodel.requests import AddSensorMeasureRequest
from airquality.iterables.responses import StationMeasureIterableResponses


def _rome_timezone():
    return tutils.get_tzinfo_from_timezone_name(tzname='Europe/Rome')


def _test_sensor_request():
    return AddSensorMeasureRequest(
        timestamp=datetime(2021, 12, 20, 12, 18, 40, tzinfo=_rome_timezone()),
        measures=[(12, 20.50), (14, 37.43), (15, 55), (16, 60)]
    )


def _mocked_validator():
    mocked_v = MagicMock()
    mocked_v.__len__.return_value = 1
    mocked_v.__iter__.return_value = [_test_sensor_request()]
    return mocked_v


def _expected_measure_record():
    ts = '2021-12-20 12:18:40+01:00'
    return f"(140, 99, 12, 20.5, '{ts}')," \
           f"(140, 99, 14, 37.43, '{ts}')," \
           f"(140, 99, 15, 55, '{ts}')," \
           f"(140, 99, 16, 60, '{ts}')"


def _test_sensor_api_param_datamodel():
    return SensorApiParamDM(
        sid=99,
        ch='fakename',
        id='fakeid',
        key='fakekey',
        last=datetime(2022, 1, 10, 9, 44)
    )


class TestAddThingspeakMeasureResponseBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._response_builder = StationMeasureIterableResponses(
            requests=_mocked_validator(),
            start_packet_id=140,
            sensor_param=_test_sensor_api_param_datamodel()
        )

# =========== TEST METHOD
    def test_create_response_to_request_of_adding_station_measures(self):
        self.assertEqual(
            len(self._response_builder),
            1
        )
        self.assertEqual(
            self._response_builder[0].measure_record,
            _expected_measure_record()
        )


if __name__ == '__main__':
    main()
