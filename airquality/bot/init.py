#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
import airquality.bot.base as base
import airquality.logger.util.decorator as log_decorator


################################ INITIALIZE BOT ################################
class InitializeBot(base.BaseBot):

    def __init__(self, log_filename: str, log_sub_dir: str):
        super(InitializeBot, self).__init__(log_filename, log_sub_dir)

    ################################ RUN METHOD ################################
    @log_decorator.log_decorator()
    def execute(self):

        # Query database sensor names
        database_sensor_names = self.sensor_type_select_wrapper.get_sensor_names()

        # Fetch API data
        sensor_data = self.fetch_wrapper.get_sensor_data()
        if not sensor_data:
            self.warning_messages.append("empty API answer => done")
            return

        # Reshape API data
        uniformed_packets = []
        for data in sensor_data:
            uniformed_packets.append(self.api2db_adapter.reshape(data))

        # Set external dependency to NameFilter
        self.sensor_data_filter.set_name_to_filter(database_sensor_names)

        # Apply NameFilter
        new_sensor_data = self.sensor_data_filter.filter(uniformed_packets)
        if not new_sensor_data:
            self.info_messages.append("all sensors are already present into the database => done")
            return

        # Query the max 'sensor_id' for knowing the 'sensor_id' during the insertion
        max_sensor_id = self.sensor_type_select_wrapper.get_max_sensor_id()

        # Execute queries on sensors
        self.insert_wrapper.initialize_sensors(sensor_data=new_sensor_data, start_id=max_sensor_id)
