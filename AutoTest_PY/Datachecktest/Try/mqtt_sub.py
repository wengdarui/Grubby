import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode('utf-8')))

def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" %(granted_qos))


client = mqtt.Client(client_id='1231321',clean_session=False)
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect("172.16.3.11", 1883, 600)
client.subscribe('DH/test/app/',qos=1)
client.loop_forever()

