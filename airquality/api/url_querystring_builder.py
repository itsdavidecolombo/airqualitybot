#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: this script defines a class for building valid URL querystring based on sensor type.
#
#################################################
import builtins
from typing import Dict, Any


KEY_VAL_SEPARATOR = "="
CONCAT_SEPARATOR = "&"


class URLQuerystringBuilder(builtins.object):
    """Class that defines @staticmethods for building the URL querystring based on sensor type"""

    @staticmethod
    def AT_querystring_from_date(api_param: Dict[str, Any]) -> str:
        """Static method that builds a URL querystring for the Atmotube sensor using 'date' field.

        -querystring:   the variable that holds the querystring
        -status_check:  binary variable used to check if all mandated parameters are provided

        If 'api_key', 'mac' or 'date' parameters missed, SystemExit exception is raised."""

        querystring = ""
        status_check = 0b000

        if api_param:
            for key, val in api_param.items():
                if key in ('api_key', 'mac', 'date', 'order'):
                    querystring += key + KEY_VAL_SEPARATOR + val + CONCAT_SEPARATOR
                else:
                    print(f"{URLQuerystringBuilder.__name__}: ignore invalid argument '{key}' in method "
                          f"'{URLQuerystringBuilder.AT_querystring_from_date.__name__}()'.")

                if key == 'api_key':
                    status_check |= 0b001
                elif key == 'mac':
                    status_check |= 0b010
                elif key == 'date':
                    status_check |= 0b100

        if status_check != 0b111:
            raise SystemExit(f"{URLQuerystringBuilder.__name__}: missing required arguments in method "
                             f"'{URLQuerystringBuilder.AT_querystring_from_date.__name__}()'.")

        querystring = querystring.strip(CONCAT_SEPARATOR)
        return querystring
