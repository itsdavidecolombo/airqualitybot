######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.logger.util.decorator as log_decorator
import airquality.command.cmd as basecmd
import airquality.api.fetchwrp as apiwrp
import airquality.api.url.purpurl as purl
import airquality.api.resp.info as resp
import airquality.database.op.ins.geo as ins
import airquality.database.op.sel.info as sel
import airquality.filter.geofilt as flt
import airquality.database.rec.info as rec


class UpdateCommand(basecmd.Command):

    def __init__(
            self,
            ub: purl.PurpleairURLBuilder,
            fw: apiwrp.FetchWrapper,
            iw: ins.StationGeoInsertWrapper,
            sw: sel.SensorInfoSelectWrapper,
            arb: resp.PurpleairSensorInfoBuilder,
            log_filename="log",
            rb_cls=rec.SensorInfoRecord
    ):
        super(UpdateCommand, self).__init__(ub=ub, fw=fw, log_filename=log_filename)
        self.insert_wrapper = iw
        self.select_wrapper = sw
        self.record_builder_cls = rb_cls
        self.api_resp_builder = arb

    # ************************************ execute ************************************
    @log_decorator.log_decorator()
    def execute(self):

        # Query database active locations
        db_responses = self.select_wrapper.select()
        if not db_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty database response => no location updated")
            return

        # Build url for fetching data from API
        url = self.url_builder.build()

        # Fetch API data
        parsed_response = self.fetch_wrapper.fetch(url=url)

        api_responses = self.api_resp_builder.build(parsed_resp=parsed_response)
        if not api_responses:
            self.log_warning(f"{UpdateCommand.__name__}: empty API response => no location updated")
            return

        # Create the Database Locations Dict
        database_active_locations = {}
        for dbresp in db_responses:
            database_active_locations[dbresp.sensor_name] = dbresp.geometry.as_text()

        # Create GeoFilter
        api_resp_filter = flt.GeoFilter(database_active_locations=database_active_locations, log_filename=self.log_filename)
        api_resp_filter.set_file_logger(self.file_logger)
        api_resp_filter.set_console_logger(self.console_logger)

        # Filter sensor data
        filtered_responses = api_resp_filter.filter(resp2filter=api_responses)
        if not filtered_responses:
            self.log_warning(f"{UpdateCommand.__name__}: all sensor locations are the same => no location updated")
            return

        # Create sensor_name - sensor_id map
        name_id_map = {}
        for dbresp in db_responses:
            name_id_map[dbresp.sensor_name] = dbresp.sensor_id

        # Build database records
        records = []
        for api_resp in filtered_responses:
            sensor_id = name_id_map[api_resp.sensor_name]
            records.append(self.record_builder_cls(info_resp=api_resp, sensor_id=sensor_id))

        # Concat update valid to timestamp for changed locations
        self.insert_wrapper.concat_update_valid_to_timestamp(records=records)

        # Concat insert new records for changed locations
        self.insert_wrapper.concat_location_query(records=records)

        # Execute all-in-one the queries (this is much safer)
        self.insert_wrapper.insert()