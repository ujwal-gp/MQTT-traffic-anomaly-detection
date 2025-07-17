# Example: MQTT Subscriber (server/aggregator)
from paho.mqtt import client as mqtt_client

broker = "localhost"
port = 1883
topic = "health/#"  # wildcard to receive all vitals
client_id = "server"

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` on topic `{msg.topic}`")

client = mqtt_client.Client(client_id)
client.on_message = on_message
client.connect(broker, port)
client.subscribe(topic)
client.loop_start()
# Run indefinitely or for demo purposes for a short period
time.sleep(5)
client.loop_stop()
