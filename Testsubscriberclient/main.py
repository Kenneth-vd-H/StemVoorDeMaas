# enable TLS client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)


import time
import paho.mqtt.client as paho
from paho import mqtt


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)



# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# Set client_id
client = paho.Client(client_id="clientReceiver", protocol=paho.MQTTv5)

client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("datareceiver", "DikkePoes44")
# connect to HiveMQ Cloud on port 8883
client.connect("dbbaa51d9b294f35a84e19c82ee01a71.s1.eu.hivemq.cloud", 8883)

# setting callbacks
client.on_subscribe = on_subscribe
client.on_message = on_message

# subscribe to a specific topic
client.subscribe("svdm/temp", qos=1)

#Available topics:
    #"svdm/temp",
    #"svdm/flow",
    #"svdm/level",
    #"svdm/pH",
    #"svdm/Liquid"

# loop_forever for simplicity, here you need to stop the loop manually
client.loop_forever()

