######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 10:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict
from abc import abstractmethod
from airquality.datamodel.apiparam import APIParam
from airquality.environment import Environment
from airquality.database.adapter import Psycopg2Adapter
from airquality.database.gateway import DatabaseGateway


class UsecaseRunner(object):
    """
    An *object* that defines a common interface for running the application UseCases.
    """

    def __init__(self, env: Environment, personality: str):
        self.env = env
        self.personality = personality

    def run(self):
        with Psycopg2Adapter(dbname=self.env.dbname,
                             user=self.env.user,
                             password=self.env.password,
                             host=self.env.host,
                             port=self.env.port) as dbadapter:
            self.process_usecases(gateway=DatabaseGateway(dbadapter=dbadapter))

    @abstractmethod
    def process_usecases(self, gateway: DatabaseGateway) -> None:
        pass


from airquality.core.apidata_builder import PurpleairAPIDataBuilder
from airquality.core.request_builder import AddPurpleairSensorRequestBuilder
from airquality.usecase.add_fixed_sensors import AddFixedSensors


class AddFixedSensorsRunner(UsecaseRunner):
    """
    A *UsecaseRunner* that defines how to run an *AddFixedSensors* UseCase.
    """

    def process_usecases(self, gateway: DatabaseGateway) -> None:
        start_sensor_id = gateway.get_max_sensor_id_plus_one()
        existing_names = gateway.get_existing_sensor_names_of_type(sensor_type=self.personality)
        datamodels = PurpleairAPIDataBuilder(url=self.env.url_template(personality=self.personality))
        requests = AddPurpleairSensorRequestBuilder(datamodel=datamodels)
        AddFixedSensors(
            output_gateway=gateway, existing_names=existing_names, start_sensor_id=start_sensor_id
        ).process(requests=requests)


from airquality.url.timeiter_url import AtmotubeTimeIterableURL
from airquality.core.apidata_builder import AtmotubeAPIDataBuilder
from airquality.core.request_builder import AddAtmotubeMeasureRequestBuilder
from airquality.usecase.add_mobile_measures import AddMobileMeasures


class AddAtmotubeMeasuresRunner(UsecaseRunner):
    """
    A *UsecaseRunner* that defines how to run the *AddMobileMeasures* UseCase.
    """

    def process_usecases(self, gateway: DatabaseGateway) -> None:
        code2id = gateway.get_measure_param_owned_by(owner=self.personality)
        apiparam = gateway.get_apiparam_of_type(sensor_type=self.personality)
        for param in apiparam:
            print(repr(param))
            for url in self.urls_of(param):
                start_packet_id = gateway.get_max_mobile_packet_id_plus_one()
                filter_ts = gateway.get_last_acquisition_of_sensor_channel(sensor_id=param.sensor_id, ch_name=param.ch_name)
                print(f"url='{url}', packet_id='{start_packet_id}', filter_ts='{filter_ts}'")
                AddMobileMeasures(
                    apiparam=param, filter_ts=filter_ts, gateway=gateway, start_packet_id=start_packet_id
                ).process(requests=self.requests_of(url=url, code2id=code2id))

    def urls_of(self, param: APIParam) -> AtmotubeTimeIterableURL:
        url_template = self.env.url_template(self.personality)
        pre_formatted_url = url_template.format(api_key=param.api_key, api_id=param.api_id, api_fmt="json")
        return AtmotubeTimeIterableURL(url=pre_formatted_url, begin=param.last_acquisition)

    def requests_of(self, url: str, code2id: Dict[str, int]) -> AddAtmotubeMeasureRequestBuilder:
        datamodels = AtmotubeAPIDataBuilder(url=url)
        return AddAtmotubeMeasureRequestBuilder(datamodel=datamodels, code2id=code2id)
