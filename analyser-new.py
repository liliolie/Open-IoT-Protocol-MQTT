import csv

import paho.mqtt.client as mqtt
import time

QoS = 0
topic = "request/delay"
payload = 5
delay = 10



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    topic = "counter/" + str(QoS) + "/" + str(delay)
    if rc == 0:
        print(topic)
        client.subscribe('counter/0/10')
        client.subscribe("$SYS/#")
    else:
        print("Connect returned result code: " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Message received with QoS=" + str(msg.qos) + ": {Topic: " + msg.topic + "}:{Payload:" + msg.payload.decode(
        "utf-8") + "}")
    with open('analyzer_0_10.csv', 'a+') as f:
        writer = csv.writer(f, delimiter=",")
        topic_row = []
        payload_row = []
        topic_row.append(msg.topic)
        payload_row.append(msg.payload.decode("utf-8"))
        writer.writerows(zip(topic_row, payload_row))



        # f.write(
        #     "Message received with QoS=" + str(msg.qos) + ": {Topic: " + msg.topic + "}:{Payload:" + msg.payload.decode(
        #         "utf-8") + "}" + "\n")

    #save data in the csv file
    # formatted_message = "Message received with QoS=" + str(
    #     msg.qos) + ": {Topic: " + msg.topic + "}:{Payload:" + msg.payload.decode(
    #     "utf-8") + "}"
    # print(formatted_message)

    # with open('analyzer.csv', 'a+') as f:
    #     f.write(
    #         "Message received with QoS=" + str(msg.qos) + ": {Topic: " + msg.topic + "}:{Payload:" + msg.payload.decode(
    #             "utf-8") + "}" + "\n")
    # with open('analyzer.csv', 'a+') as f:
    #     f.write(
    #         msg.payload.decode("utf-8") + "\n")



# create the client
client = mqtt.Client(client_id="3310a")
client.on_connect = on_connect


client.on_message = on_message
# client.on_subscribe = on_subscribe


# set username and password
client.username_pw_set("student", "33102021")

# connect to Cloud on port
client.connect("c4891771.us-east-1.emqx.cloud", 15858)
client.loop_start()
client.publish(topic,payload=10)
time.sleep(120)
client.loop_stop()
