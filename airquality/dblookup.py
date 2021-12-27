######################################################
#
# Author: Davide Colombo
# Date: 22/12/21 20:24
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
SENSOR_COLS = ['sensor_type', 'sensor_name']
MEASURE_PARAM_COLS = ['param_owner', 'param_code', 'param_name', 'param_unit']

from collections import namedtuple


class MeasureParamLookup(namedtuple('MeasureParamLookup', MEASURE_PARAM_COLS)):
    """A class that wraps a database lookup to 'measure_param' table just to avoid using list indexing."""

    def __repr__(self):
        return f"{type(self).__name__}(param_owner={self.param_owner}, param_code={self.param_code}, " \
               f"param_name={self.param_name}, param_unit={self.param_unit})"


class SensorLookup(namedtuple('SensorLookup', SENSOR_COLS)):
    """A class that wraps a database lookup to 'sensor' table just to avoid using list indexing."""

    def __repr__(self):
        return f"{type(self).__name__}(sensor_type={self.sensor_type}, sensor_name={self.sensor_name})"