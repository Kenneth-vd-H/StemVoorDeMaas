
class Sensor:
    hardware_connection = False

    def __init__(self, name):
        self.name = name
        self.value = None

    @staticmethod
    def check_hardware_connection():
        Sensor.hardware_connection = True
        return Sensor.hardware_connection

    def set_reading(self, value):
        self.value = value

    def get_reading(self):
        return self.value
