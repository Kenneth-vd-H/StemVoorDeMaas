from sensor_data import Sensor
from database_connection import Dbconnection


def main():
    sensor1 = Sensor("temperatuur")
    sensor2 = Sensor("waterflow")
    sensor3 = Sensor("waterpeil")
    sensor4 = Sensor("Ph-waarde")

    sensor1.set_reading(12.3)
    sensor2.set_reading(13.7)
    sensor3.set_reading(44.5)
    sensor4.set_reading(33.2)

    hardware_con = Sensor.check_hardware_connection()
    db_con = Dbconnection.check_database_connection()

    while hardware_con and db_con:
        hardware_con = Sensor.check_hardware_connection()
        db_con = Dbconnection.check_database_connection()
        Dbconnection.query_data(sensor1.get_reading(), sensor2.get_reading(), sensor3.get_reading(), sensor4.get_reading())


if __name__ == "__main__":
    main()
