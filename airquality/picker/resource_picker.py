#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 16:42
# @Description: this script defines a class for picking resources from all the parsed resources.
#
#################################################
import builtins
from typing import Dict, Any


LOGGER_SECTION = "logger"
SERVER_SECTION = "server"
PERSONALITY_SECTION  = "personality"
API_ADDRESS_SECTION = "api_address"


class ResourcePicker(builtins.object):


    @staticmethod
    def pick_db_conn_properties_from_personality(parsed_resources: Dict[str, Any], bot_personality: str) -> Dict[str, Any]:
        """Static method that picks the database properties from the parsed resources.

        If 'server' section is missing in 'properties/resources.json' file, SystemExit exception is raised.

        If 'bot_personality' is invalid, SystemExit exception is raised."""

        if parsed_resources.get(PERSONALITY_SECTION, None) is None:
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"missing '{PERSONALITY_SECTION}' section in resource file in method "
                             f"'{ResourcePicker.pick_db_conn_properties_from_personality.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if parsed_resources.get(SERVER_SECTION, None) is None:
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"missing '{SERVER_SECTION}' section in resource file in method "
                             f"'{ResourcePicker.pick_db_conn_properties_from_personality.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if bot_personality not in parsed_resources[PERSONALITY_SECTION].keys():
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"don't recognize personality '{bot_personality}' in method "
                             f"'{ResourcePicker.pick_db_conn_properties_from_personality.__name__}()'."
                             f"Check your 'properties/resources.json' file.")


        settings = parsed_resources[SERVER_SECTION].copy()
        settings["username"] = parsed_resources[PERSONALITY_SECTION][f"{bot_personality}"]["username"]
        settings["password"] = parsed_resources[PERSONALITY_SECTION][f"{bot_personality}"]["password"]
        return settings

    @staticmethod
    def pick_api_address_from_number(parsed_resources: Dict[str, Any], bot_personality: str, api_address_number: str) -> str:

        if parsed_resources.get(API_ADDRESS_SECTION, None) is None:
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"missing '{API_ADDRESS_SECTION}' section in resource file in method "
                             f"'{ResourcePicker.pick_api_address_from_number.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if bot_personality not in parsed_resources[API_ADDRESS_SECTION].keys():
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"don't recognize personality '{bot_personality}' in method "
                             f"'{ResourcePicker.pick_api_address_from_number.__name__}()'."
                             f"Check your 'properties/resources.json' file.")

        if api_address_number not in parsed_resources[API_ADDRESS_SECTION][f"{bot_personality}"].keys():
            raise SystemExit(f"{ResourcePicker.__name__}: "
                             f"don't recognize api address number '{bot_personality}' in method "
                             f"'{ResourcePicker.pick_api_address_from_number.__name__}()'."
                             f"Check your 'properties/resources.json' file.")


        return parsed_resources[API_ADDRESS_SECTION][f"{bot_personality}"][f"{api_address_number}"]