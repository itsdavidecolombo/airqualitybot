######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 02/11/21 12:29
# Description: this script defines a class for building geometry type string based on API parameters
#
######################################################
from typing import Dict, Any
from abc import ABC, abstractmethod
from airquality.constants.shared_constants import EXCEPTION_HEADER


class PostGISGeometry(ABC):

    @abstractmethod
    def get_database_string(self, packet: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def get_geomtype_string(self, packet: Dict[str, Any]) -> str:
        pass


class PostGISPoint(PostGISGeometry):

    def get_database_string(self, packet: Dict[str, Any]) -> str:
        try:
            return f"ST_GeomFromText('POINT({packet['lng']} {packet['lat']})', 26918)"
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {PostGISPoint.__name__} missing required key={ke!s}")

    def get_geomtype_string(self, packet: Dict[str, Any]) -> str:
        try:
            return f"POINT({packet['lng']} {packet['lat']})"
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {PostGISPoint.__name__} missing required key={ke!s}")
