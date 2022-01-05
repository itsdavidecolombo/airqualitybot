######################################################
#
# Author: Davide Colombo
# Date: 30/12/21 15:01
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from airquality.core.response_builder import AddFixedSensorResponseBuilder, AddMobileMeasureResponseBuilder, \
    AddStationMeasuresResponseBuilder, AddPlacesResponseBuilder, AddOpenWeatherMapDataResponseBuilder
from airquality.database.adapter import DatabaseAdapter
from airquality.datamodel.apidata import WeatherCityData, CityOfGeoarea
from airquality.datamodel.apiparam import APIParam
from airquality.datamodel.service_param import ServiceParam
from typing import Set, Dict, List
from datetime import datetime


class DatabaseGateway(object):
    """
    An *object* class that moderates the interaction between the system and the database.
    """

    def __init__(self, dbadapter: DatabaseAdapter):
        self.dbadapter = dbadapter

    def get_existing_sensor_names_of_type(self, sensor_type: str) -> Set[str]:
        rows = self.dbadapter.fetchall(
            f"SELECT sensor_name FROM level0_raw.sensor WHERE sensor_type ILIKE '%{sensor_type}%';")
        return {row[0] for row in rows}

    def get_max_sensor_id_plus_one(self) -> int:
        row = self.dbadapter.fetchone("SELECT MAX(id) FROM level0_raw.sensor;")
        return 1 if row[0] is None else row[0] + 1

    def insert_sensors(self, responses: AddFixedSensorResponseBuilder):
        sensor_query = "INSERT INTO level0_raw.sensor VALUES "
        apiparam_query = "INSERT INTO level0_raw.sensor_api_param (sensor_id, ch_key, ch_id, ch_name, last_acquisition) VALUES "
        geolocation_query = "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) VALUES "
        for response in responses:
            sensor_query += response.sensor_record + ','
            apiparam_query += response.apiparam_record + ','
            geolocation_query += response.geolocation_record + ','

        self.dbadapter.execute(
            f"{sensor_query.strip(',')}; {apiparam_query.strip(',')}; {geolocation_query.strip(',')};")

    def get_measure_param_owned_by(self, owner: str) -> Dict[str, int]:
        rows = self.dbadapter.fetchall(
            f"SELECT id, param_code FROM level0_raw.measure_param WHERE param_owner ILIKE '%{owner}%';")
        return {code: ident for ident, code in rows}

    def insert_mobile_sensor_measures(self, responses: AddMobileMeasureResponseBuilder):
        measure_query = "INSERT INTO level0_raw.mobile_measurement (packet_id, param_id, param_value, timestamp, geom) VALUES "
        measure_query += ','.join(resp.measure_record for resp in responses)
        self.dbadapter.execute(f"{measure_query};")

    def update_last_acquisition(self, timestamp: str, sensor_id: int, ch_name: str):
        self.dbadapter.execute(
            f"UPDATE level0_raw.sensor_api_param SET last_acquisition = '{timestamp}' "
            f"WHERE sensor_id = {sensor_id} AND ch_name = '{ch_name}';"
        )

    def get_apiparam_of_type(self, sensor_type: str) -> List[APIParam]:
        rows = self.dbadapter.fetchall(
            "SELECT a.sensor_id, a.ch_key, a.ch_id, a.ch_name, a.last_acquisition FROM level0_raw.sensor_api_param AS a "
            f"INNER JOIN level0_raw.sensor AS s ON s.id = a.sensor_id WHERE s.sensor_type ILIKE '%{sensor_type}%';"
        )
        return [APIParam(sensor_id=sid, api_key=key, api_id=ident, ch_name=name, last_acquisition=last)
                for sid, key, ident, name, last in rows]

    def get_max_mobile_packet_id_plus_one(self) -> int:
        row = self.dbadapter.fetchone("SELECT MAX(packet_id) FROM level0_raw.mobile_measurement;")
        return 1 if row[0] is None else row[0] + 1

    def get_last_acquisition_of_sensor_channel(self, sensor_id: int, ch_name: str) -> datetime:
        return self.dbadapter.fetchone(
            f"SELECT last_acquisition FROM level0_raw.sensor_api_param WHERE sensor_id = {sensor_id} AND ch_name = '{ch_name}';"
        )[0]

    def insert_station_measures(self, responses: AddStationMeasuresResponseBuilder):
        query = "INSERT INTO level0_raw.station_measurement (packet_id, sensor_id, param_id, param_value, timestamp) VALUES "
        query += ','.join(resp.measure_record for resp in responses)
        self.dbadapter.execute(f"{query};")

    def get_max_station_packet_id_plus_one(self) -> int:
        row = self.dbadapter.fetchone("SELECT MAX(packet_id) FROM level0_raw.station_measurement;")
        return 1 if row[0] is None else row[0] + 1

    def get_service_id_from_name(self, service_name: str) -> int:
        return self.dbadapter.fetchone(
            f"SELECT id FROM level0_raw.service WHERE service_name ILIKE '%{service_name}%';"
        )[0]

    def get_poscodes_of_country(self, country_code) -> Set[str]:
        rows = self.dbadapter.fetchall(
            f"SELECT postal_code FROM level0_raw.geographical_area WHERE country_code = '{country_code}';"
        )
        return {row[0] for row in rows}

    def insert_places(self, responses: AddPlacesResponseBuilder):
        query = "INSERT INTO level0_raw.geographical_area " \
                "(service_id, postal_code, country_code, place_name, province, state, geom) VALUES "
        query += ','.join(resp.place_record for resp in responses)
        self.dbadapter.execute(f"{query};")

    def get_service_apiparam_of(self, service_name: str) -> List[ServiceParam]:
        rows = self.dbadapter.fetchall(
            "SELECT p.api_key, p.n_requests FROM level0_raw.service_api_param AS p INNER JOIN level0_raw.service AS s "
            f"ON s.id = p.service_id WHERE s.service_name ILIKE '%{service_name}%';"
        )
        return [ServiceParam(api_key=api_key, n_requests=nreq) for api_key, nreq in rows]

    def get_weather_conditions(self) -> Dict[int, Dict[str, int]]:
        rows = self.dbadapter.fetchall(
            "SELECT id, code, icon FROM level0_raw.weather_condition;"
        )
        weather_map = {code: {} for id_, code, icon in rows}
        for id_, code, icon in rows:
            weather_map[code][icon] = id_
        return weather_map

    def get_geolocation_of(self, city: WeatherCityData) -> CityOfGeoarea:
        row = self.dbadapter.fetchone(
            f"SELECT id, ST_X(geom), ST_Y(geom) FROM level0_raw.geographical_area "
            f"WHERE country_code = '{city.country_code}' AND place_name = '{city.place_name}';"
        )
        if row is None:
            raise ValueError(
                f"{type(self).__name__} missing row in 'geographical_area' table corresponding to {city!r}")
        return CityOfGeoarea(geoarea_id=row[0], longitude=row[1], latitude=row[2])

    def delete_all_from_hourly_weather_forecast(self):
        self.dbadapter.execute("DELETE FROM level0_raw.hourly_forecast;")

    def delete_all_from_daily_weather_forecast(self):
        self.dbadapter.execute("DELETE FROM level0_raw.daily_forecast;")

    def insert_weather_data(self, responses: AddOpenWeatherMapDataResponseBuilder):
        current_weather_data_query = \
            "INSERT INTO level0_raw.current_weather (service_id, geoarea_id, weather_id, temperature, pressure, " \
            "humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES "

        hourly_weather_data_query = \
            "INSERT INTO level0_raw.hourly_forecast (service_id, geoarea_id, weather_id, temperature, pressure, " \
            "humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES "

        daily_weather_data_query = \
            "INSERT INTO level0_raw.daily_forecast (service_id, geoarea_id, weather_id, temperature, min_temp, max_temp, " \
            "pressure, humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES "

        for resp in responses:
            current_weather_data_query += resp.current_weather_record + ','
            hourly_weather_data_query += resp.hourly_forecast_record + ','
            daily_weather_data_query += resp.daily_forecast_record + ','

        self.dbadapter.execute(f"{current_weather_data_query.strip(',')}; "
                               f"{hourly_weather_data_query.strip(',')}; "
                               f"{daily_weather_data_query.strip(',')};")

    def __repr__(self):
        return f"{type(self).__name__}(dbadapter={self.dbadapter!r})"
