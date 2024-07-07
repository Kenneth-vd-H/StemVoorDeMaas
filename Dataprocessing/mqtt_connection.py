# enable TLS client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)


import paho.mqtt.client as paho
from paho import mqtt


class MqttConnection:
    # Test callbacks

    def __init__(self, client_id, broker, port, username, pwd, topic, qos=1):
        self.client = paho.Client(client_id=client_id, protocol=paho.MQTTv5)
        self.broker = broker
        self.port = port
        self.username = username
        self.password = pwd
        self.topic = topic
        self.qos = qos


        #Set callbacks
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message


        #Enable TLS for secure connection
        self.client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)


        #Set user credentials
        self.client.username_pw_set(self.username, self.password)


    #Callback function definitions
    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("CONNACK received with code %s." % rc)

    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


    #Method definitions
    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self, payload):
        self.client.publish(self.topic, payload=payload, qos=self.qos)


    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
