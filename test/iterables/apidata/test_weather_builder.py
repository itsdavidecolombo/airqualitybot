######################################################
#
# Author: Davide Colombo
# Date: 29/12/21 20:06
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import test._test_utils as tutils
from unittest import TestCase, main
from airquality.iterables.fromapi import OpenweathermapIterableDatamodels


def _test_openweathermap_json_response():
    return tutils.get_json_response_from_file(
        filename='openweather_data.json'
    )


class TestOpenweathermapAPIDataBuilder(TestCase):

# =========== SETUP METHOD
    def setUp(self) -> None:
        self._builder = OpenweathermapIterableDatamodels(
            json_response=_test_openweathermap_json_response()
        )

# =========== TEST METHOD
    def test_create_openweathermap_data(self):
        self.assertEqual(len(self._builder), 1)
        self._assert_current_weather()
        self._assert_hourly_forecast()
        self._assert_daily_forecast()
        self._assert_weather_alert()

# =========== SUPPORT METHODS
    def _assert_weather_alert(self):
        alerts = self._builder[0].alerts
        self.assertEqual(len(alerts), 1)

        self.assertEqual(alerts[0].sender_name, 'Fake sender')
        self.assertEqual(alerts[0].alert_event, 'Fake event')
        self.assertEqual(alerts[0].alert_begin, 1643047200)
        self.assertEqual(alerts[0].alert_until, 1643101140)
        self.assertEqual(alerts[0].description, 'Fake description')

    def _assert_weather(self, weather):
        self.assertEqual(weather.id, 804)
        self.assertEqual(weather.icon, "04d")
        self.assertEqual(weather.main, "Clouds")
        self.assertEqual(weather.description, "overcast clouds")

    def _assert_current_weather(self):
        current = self._builder[0].current
        self._assert_weather(weather=current.weather[0])
        self.assertEqual(current.dt, 1641217631)
        self.assertEqual(current.sunrise, 1641193337)
        self.assertEqual(current.sunset, 1641225175)
        self.assertEqual(current.temp, 8.84)
        self.assertIsNone(current.temp_min)
        self.assertIsNone(current.temp_max)
        self.assertEqual(current.pressure, 1018)
        self.assertEqual(current.humidity, 81)
        self.assertEqual(current.wind_speed, 0.59)
        self.assertEqual(current.wind_deg, 106)
        self.assertIsNone(current.rain)
        self.assertIsNone(current.snow)
        self.assertIsNone(current.pop)

    def _assert_hourly_forecast(self):
        forecast_list = self._builder[0].hourly_forecast
        self.assertEqual(len(forecast_list), 1)

        hourly1 = forecast_list[0]
        self._assert_weather(weather=hourly1.weather[0])
        self.assertEqual(hourly1.dt, 1641214800)
        self.assertEqual(hourly1.temp, 9.21)
        self.assertIsNone(hourly1.temp_min)
        self.assertIsNone(hourly1.temp_max)
        self.assertEqual(hourly1.pressure, 1018)
        self.assertEqual(hourly1.humidity, 80)
        self.assertEqual(hourly1.wind_speed, 0.33)
        self.assertEqual(hourly1.wind_deg, 186)
        self.assertEqual(hourly1.rain, 0.21)
        self.assertEqual(hourly1.pop, 0)
        self.assertIsNone(hourly1.snow)
        self.assertIsNone(hourly1.sunrise)
        self.assertIsNone(hourly1.sunset)

    def _assert_daily_forecast(self):
        forecast_list = self._builder[0].daily_forecast
        self.assertEqual(len(forecast_list), 1)

        daily1 = forecast_list[0]
        self._assert_weather(weather=daily1.weather[0])
        self.assertEqual(daily1.dt, 1641207600)
        self.assertEqual(daily1.temp, 9.25)
        self.assertEqual(daily1.temp_min, 5.81)
        self.assertEqual(daily1.temp_max, 9.4)
        self.assertEqual(daily1.pressure, 1019)
        self.assertEqual(daily1.humidity, 83)
        self.assertEqual(daily1.wind_speed, 2.72)
        self.assertEqual(daily1.wind_deg, 79)
        self.assertEqual(daily1.pop, 0.01)
        self.assertIsNone(daily1.rain)
        self.assertIsNone(daily1.snow)
        self.assertIsNone(daily1.sunset)
        self.assertIsNone(daily1.sunrise)


if __name__ == '__main__':
    main()
