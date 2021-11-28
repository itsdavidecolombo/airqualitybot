######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 10:43
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import sys
from typing import List, Tuple
import airquality.logger.util.log as log
import airquality.command.fetch.fact as fetchfact
import airquality.command.init.fact as initfact
import airquality.command.update.fact as updtfact
import airquality.file.util.loader as fl
import airquality.database.conn.fact as dbfact
import airquality.database.conn.shutdown as dbshutdown

PROPERTIES_DIR = "properties"                           # name of the directory that contains all the project file
ENV_FILE_PATH = f"{PROPERTIES_DIR}/.env"                # name of the environment file, that keeps sensitive data
API_FILE_PATH = f"{PROPERTIES_DIR}/api.json"            # name of the API configuration file
QUERY_FILE_PATH = f"{PROPERTIES_DIR}/query.json"        # name of the SQL query statements file


# Create error logger and debugger
error_logger = log.get_file_logger(file_path='log/errors.log', logger_name="errors")
console_logger = log.get_console_logger(use_color=True)


def main():
    try:
        command_name, sensor_type = get_commandline_arguments(sys.argv[1:])

        # ----------- GET COMMAND FACTORY CLASS -----------
        command_factory_cls = get_command_factory_cls(command_name=command_name, sensor_type=sensor_type)

        log_filename = sensor_type
        logger_file_path = f"log/{command_name}/{log_filename}.log"
        logger_name = f"{sensor_type}_{command_name}_logger"

        # ----------- CREATE COMMAND's COMMON OBJECTS -----------
        fl.load_environment_file(file_path=ENV_FILE_PATH, sensor_type=sensor_type)
        api_file = fl.load_structured_file(file_path=API_FILE_PATH, path_to_object=[sensor_type], log_filename=log_filename)
        query_file = fl.load_structured_file(file_path=QUERY_FILE_PATH, log_filename=log_filename)
        database_conn = dbfact.get_database_adapter(connection_string=os.environ['DBCONN'], log_filename=log_filename)
        database_conn.open_conn()

        # ----------- COMMAND FACTORY -----------
        command_factory = command_factory_cls(
            api_file=api_file, query_file=query_file, conn=database_conn, log_filename=log_filename
        )

        file_logger = log.get_file_logger(file_path=logger_file_path, logger_name=logger_name)
        command_factory.set_file_logger(logger=file_logger)
        command_factory.set_console_logger(logger=console_logger)

        # ----------- GET COMMAND OBJECT -----------
        cmd_obj = command_factory.create_command(sensor_type=sensor_type)
        cmd_obj.execute()

        # ----------- SAFE SHUTDOWN -----------
        safe_shutdown()

    except (SystemExit, AttributeError, KeyError) as ex:
        console_logger.error(f"{ex!s}")
        error_logger.error(f"{ex!s}")
        sys.exit(1)
    finally:
        safe_shutdown()


################################ get_commandline_arguments ################################
def get_commandline_arguments(args: List[str]) -> Tuple[str, str]:

    function_name = get_commandline_arguments.__name__
    program_usage = "USAGE: python(version) -m airquality command_name sensor_type"

    if not args:
        raise SystemExit(f"{function_name}(): bad usage => missing required arguments. {program_usage}")
    if len(args) != 2:
        raise SystemExit(f"{function_name}(): bad usage => wrong number of argument. {program_usage}")

    command_name = args[0]
    sensor_type = args[1]

    valid_commands = ["init", "update", "fetch"]
    if command_name not in valid_commands:
        raise SystemExit(f"{function_name}: bad command => VALID COMMANDS: [{'|'.join(c for c in valid_commands)}]")

    valid_types = ["atmotube", "purpleair", "thingspeak"]
    if sensor_type not in valid_types:
        raise SystemExit(f"{function_name}(): bad type => VALID TYPES: [{'|'.join(tp for tp in valid_types)}]")

    return command_name, sensor_type


################################ get_command_factory_cls ################################
def get_command_factory_cls(command_name: str, sensor_type: str):

    if command_name == 'init':
        return initfact.get_init_factory_cls(sensor_type=sensor_type)
    elif command_name == 'update':
        return updtfact.get_update_factory_cls(sensor_type=sensor_type)
    elif command_name == 'fetch':
        return fetchfact.get_fetch_factory_cls(sensor_type=sensor_type)


################################ safe_shutdown ################################
def safe_shutdown():
    dbshutdown.shutdown()
    log.logging.shutdown()
