import time
import serial
import json

from sensor_data import Sensor
from mqtt_connection import MqttConnection



#Initialize serial connection constants
SERIAL_PORT = 'COM3' #May be different in other machines. Replace with correct port if necessary
BAUD_RATE = 115200


def main():
    #Initialize sensors
    sensors = [
        Sensor("temperature"),
        Sensor("flow_rate"),
        Sensor("water_level"),
        Sensor("pH"),
        Sensor("output_liquid_quantity")
    ]

    #Create MQTT topics for each sensor
    topics = [
        "svdm/temp",
        "svdm/flow",
        "svdm/level",
        "svdm/pH",
        "svdm/Liquid"
    ]


    #Initialize MQTT subscriber client
    mqtt_client1 = MqttConnection(
        "clientSender1",
        "dbbaa51d9b294f35a84e19c82ee01a71.s1.eu.hivemq.cloud",
        8883,
        "Stemvoordemaas",
        "ZupaSmeltah5"
    )


    #Initialize connection to MQTT broker
    mqtt_client1.connect()

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            time.sleep(2)# Wait for serial connection

            while True:
                #get data from serial port in Json format
                json_data = read_from_arduino(ser)
                #Check if object is empty
                if json_data:
                    #Publish sensor data to dedicated topics
                    for sensor, topic in zip(sensors, topics):
                        sensor.set_reading(json_data.get(sensor.get_name()))
                        mqtt_client1.publish(topic, sensor.get_reading())
                time.sleep(1)

    except KeyboardInterrupt:
        #Stop running code if key is pressed
        print("Disconnect from broker")
    finally:
        #Disconnect client from MQTT broker
        mqtt_client1.disconnect()


def read_from_arduino(ser):
    try:
        line = ser.readline().decode('utf-8').rstrip()
        #Check if line is empty
        if line:
            try:
                #create new json object
                data = json.loads(line)
                return data
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
    except serial.SerialException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
