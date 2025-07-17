# Example: MQTT Publisher (client/device)
from paho.mqtt import client as mqtt_client
import time, json

broker = "localhost"  # or broker address
port = 1883
topic = "health/vitals"
client_id = "client1"

def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.connect(broker, port)
    return client

def publish_data(client):
    client.loop_start()
    for t in range(5):
        payload = json.dumps({"time": t, "HR": 60 + t, "SpO2": 98 - 0.1*t})
        result = client.publish(topic, payload)
        status = result[0]
        if status == 0:
            print(f"Sent `{payload}` to topic `{topic}`")
        time.sleep(1)
    client.loop_stop()

if __name__ == "__main__":
    client = connect_mqtt()
    publish_data(client)
