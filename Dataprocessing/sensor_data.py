class Sensor:
    hardware_connection = False

    def __init__(self, name):
        self.name = name
        self.value = None

    def get_name(self):
        return self.name

    def set_reading(self, value):
        self.value = value

    def get_reading(self):
        return self.value
