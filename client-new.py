import paho.mqtt.client as mqtt
import time

counter = 0
QoS = 0
delay = 100
interrupt = False
start = time.time()


# The callback for when the client receives a  response from the server.
def on_connect(client, userdata, flags, rc):
    global QoS
    global delay
    global topic
    topic = "counter/" + str(QoS) + "/" + str(delay)
    if rc == 0:
        print("Connected successfully")
        client.subscribe("request/qos")
        client.subscribe("request/delay")
    else:
        print("Connect returned result code: " + str(rc))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global QoS
    global delay
    global interrupt
    global topic
    global counter

    if (msg.topic != "request/qos" and msg.topic != "request/delay"):
        print(
            "Message received with QoS=" + str(msg.qos) + ":{Payload:" + msg.payload.decode(
                "utf-8") + "}")

    # change the value of qos
    if (msg.topic == "request/qos"):
        QoS = int(msg.payload.decode("utf-8"))
        topic = "counter/" + str(QoS) + "/" + str(delay)
        counter=0
        interrupt = True

    # change the value of delay
    if (msg.topic == "request/delay"):
        delay = float(msg.payload.decode("utf-8"))
        print("Delay set to: " + str(delay))
        topic = "counter/" + str(QoS) + "/" + str(delay)
        counter=0
        interrupt = True


# The callback for when subscribed to a topic
# def on_subscribe(client, userdata, mid, granted_qos):
#     print("Subscribe with mid "+str(mid)+" received.")


# create the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.on_subscribe = on_subscribe

# set username and password
client.username_pw_set("student", "33102021")

# connect to Cloud on port
client.connect("c4891771.us-east-1.emqx.cloud", 15858)


client.loop_start()
# client.max_inflight_messages_set(5000,000)
# Running the program indefinitely until Keyboard Interrupt
try:
    # while not (time.time() - start)>=20*60:
    while True:
        if interrupt == True:
            print("Sleeping for 2.5 minutes")
            time.sleep(2.5)
            interrupt = False
            counter = 0
            print("Woke up from sleeping")

        topic = "counter/" + str(QoS) + "/" + str(delay)
        print(topic)
        payload = str(counter)
        client.publish(topic,payload, qos=QoS)
        counter += 1
        time.sleep(delay/1000)


except KeyboardInterrupt:
    print("Exiting")
    client.disconnect()
    time.sleep(.1)
    client.loop_stop()
    print("See you next time.")



# import paho.mqtt.client as mqtt
# import time
#
# # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected successfully")
#     else:
#         print("Connect returned result code: " + str(rc))
#
# # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print("Received message: " + msg.topic + " -> " + msg.payload.decode("utf-8"))
#
# # create the client
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
#
# # set username and password
# client.username_pw_set("student", "33102021")
#
# # connect to Cloud on port
# client.connect("c4891771.us-east-1.emqx.cloud", 15858)
#
# # subscribe to the topic "my/test/topic"
# client.subscribe("my/test/topic")
#
# # publish "Hello" to the topic "my/test/topic"
# client.publish("my/test/topic", "Hello")
#
# # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
# client.loop_forever()