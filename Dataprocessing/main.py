import time

import sensor_data
from sensor_data import Sensor
from mqtt_connection import MqttConnection
import serial
import json

#from database_connection import Dbconnection

SERIAL_PORT = 'COM3'  # Replace with your serial port
BAUD_RATE = 115200


def main():
    sensor1 = Sensor("temperature")
    sensor2 = Sensor("waterflow")
    sensor3 = Sensor("waterlevel")
    sensor4 = Sensor("Ph-level")
    sensor5 = Sensor("liquid")

    hardware_con = Sensor.check_hardware_connection()
    mqtt_client1 = MqttConnection(
        "clientSender1",
        "dbbaa51d9b294f35a84e19c82ee01a71.s1.eu.hivemq.cloud",
        8883,
        "Stemvoordemaas",
        "ZupaSmeltah5",
        "svdm/temp")
    mqtt_client2 = MqttConnection(
        "clientSender2",
        "dbbaa51d9b294f35a84e19c82ee01a71.s1.eu.hivemq.cloud",
        8883,
        "Stemvoordemaas",
        "ZupaSmeltah5",
        "svdm/flow")
    mqtt_client3 = MqttConnection(
        "clientSender3",
        "dbbaa51d9b294f35a84e19c82ee01a71.s1.eu.hivemq.cloud",
        8883,
        "Stemvoordemaas",
        "ZupaSmeltah5",
        "svdm/level")
    mqtt_client4 = MqttConnection(
        "clientSender4",
        "dbbaa51d9b294f35a84e19c82ee01a71.s1.eu.hivemq.cloud",
        8883,
        "Stemvoordemaas",
        "ZupaSmeltah5",
        "svdm/pH")
    mqtt_client5 = MqttConnection(
        "clientSender5",
        "dbbaa51d9b294f35a84e19c82ee01a71.s1.eu.hivemq.cloud",
        8883,
        "Stemvoordemaas",
        "ZupaSmeltah5",
        "svdm/Liquid")

    #db_con = Dbconnection.check_database_connection()
    mqtt_client1.connect()
    mqtt_client2.connect()
    mqtt_client3.connect()
    mqtt_client4.connect()
    mqtt_client5.connect()

    try:
        while hardware_con:
            jsondata = read_from_arduino(SERIAL_PORT, BAUD_RATE)
            print(jsondata)
            sensor1.set_reading(jsondata["temperature"])
            sensor2.set_reading(jsondata["flow_rate"])
            sensor3.set_reading(jsondata["water_level"])
            sensor4.set_reading(jsondata["pH"])
            sensor5.set_reading(jsondata["output_liquid_quantity"])
            #hardware_con = Sensor.check_hardware_connection()
            mqtt_client1.publish(sensor1.get_reading())
            mqtt_client2.publish(sensor2.get_reading())
            mqtt_client3.publish(sensor3.get_reading())
            mqtt_client4.publish(sensor4.get_reading())
            mqtt_client5.publish(sensor5.get_reading())
            time.sleep(1)

    except KeyboardInterrupt:
        print("Disconnect from broker")
    finally:
        mqtt_client1.disconnect()
        mqtt_client2.disconnect()
        mqtt_client3.disconnect()
        mqtt_client4.disconnect()
        mqtt_client5.disconnect()


def read_from_arduino(serial_port, baud_rate, timeout=1):
    try:
        # Open the serial port
        ser = serial.Serial(serial_port, baud_rate, timeout=timeout)
        time.sleep(2)  # Wait for the connection to establish

        # Read a line from the serial port
        line = ser.readline().decode('utf-8').rstrip()
        if line:
            try:
                # Parse the JSON data
                data = json.loads(line)
                return data
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Exiting the program.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed.")


if __name__ == "__main__":
    serial_port = 'COM3'  # Replace with your serial port
    baud_rate = 9600


if __name__ == "__main__":
    main()
