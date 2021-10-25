#################################################
#
# @Author: davidecolombo
# @Date: lun, 25-10-2021, 16:43
# @Description: this script defines the constants shared in all modules of the project
#
#################################################


################################ DEFINE VALID PERSONALITIES FOR 'SENSOR AT LOCATION' ################################

VALID_PERSONALITIES = ('purpleair', 'atmotube')
SENSOR_AT_LOCATION_PERSONALITIES = ('purpleair',)

################################ PATH OF THE FILES USED IN THE PROJECT ################################

API_FILE    = "properties/api.json"
SERVER_FILE = "properties/server.json"
QUERY_FILE  = "properties/sql_query.json"

################################ OUTPUT FORMAT CONSTANTS ################################

DEBUG_HEADER = "[DEBUG]:"
INITIALIZE_USAGE = "USAGE: python -m initialize [-d or --debug] personality"

################################ EMPTY CONSTANTS ################################

EMPTY_STRING = ""
EMPTY_LIST   = []
EMPTY_DICT   = {}

################################ VALID API PARAMETERS ################################

ATMOTUBE_API_PARAMETERS = ('api_key', 'mac', 'date', 'order')

################################ PICKER-TO-QUERY_BUILDER CONSTANTS ################################

PICKER2SQLBUILDER_PARAM_ID  = "par_id"
PICKER2SQLBUILDER_SENSOR_ID = "sens_id"
PICKER2SQLBUILDER_PARAM_VAL = "par_val"
PICKER2SQLBUILDER_TIMESTAMP = "ts"
PICKER2SQLBUILDER_GEOMETRY  = "geom"

################################ MESSAGE ################################

SENSOR_NAME = "name"
PURPLE_AIR_API_PARAM = ("primary_id_a", "primary_key_a", "primary_id_b", "primary_key_b",
                        "secondary_id_a", "secondary_key_a", "secondary_id_b", "secondary_key_b")
PURPLE_AIR_GEO_PARAM = ("latitude", "longitude")

################################ GEOMETRY BUILDER CONSTANTS ################################

GEOMBUILDER_LATITUDE  = "latitude"
GEOMBUILDER_LONGITUDE = "longitude"

################################ POSTGIS GEOMETRY TYPE ################################

GEO_TYPE_ST_POINT_2D = "POINT({lon} {lat})"

################################ POSTGIS SRID CONSTANTS ################################

EPSG_SRID = 26918

################################ DATETIME REGULAR EXPRESSION PATTERN ################################

ATMOTUBE_DATETIME_REGEX_PATTERN = r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d+Z'
SQL_TIMESTAMP_REGEX_PATTERN     = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'

################################ DATETIME FORMAT FOR DATETIME2STR CONVERSION ################################

DATETIME2SQLTIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"