import threading

class CommunicationThread(threading.Thread):
    def __init__(self, sensors_message_parser, sensors_repo, sensor_update_event, bluetooth_communicator):
        threading.Thread.__init__(self)
        self.__sensors_message_parser = sensors_message_parser
        self.__sensors_repo = sensors_repo
        self.__sensor_update_event = sensor_update_event
        self.__bluetooth_communicator = bluetooth_communicator
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            self.__bluetooth_communicator.listen(self.__sensors_message_parser.is_buffer_parsable,
                                                 self.__sensor_callback)
        self.__bluetooth_communicator.disconnect()

    def __sensor_callback(self, message):
        data = self.__sensors_message_parser.parse_sensors_string(message)
        for sensorName, sensorValue in data.iteritems():
            self.__sensors_repo.set_sensor(sensorName, sensorValue)
            self.__sensor_update_event.send(sensorName, sensorValue)
