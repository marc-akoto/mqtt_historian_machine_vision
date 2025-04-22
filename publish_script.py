import time
import base64
import paho.mqtt.client as mqtt  # Needed for protocol enum
from paho.mqtt.client import Client, CallbackAPIVersion

# MQTT connection settings
broker = '192.168.1.111'  # EMQX container IP
port = 1883
topic = "images/defect"
client_id = 'python-publisher'

image_paths = ['./good.jpg', './bad.jpg']  # Alternating images

def connect_mqtt():
    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            print("✅ Successfully connected to MQTT broker")
        else:
            print(f"❌ Failed to connect, reason code {reason_code}")

    client = Client(
        client_id=client_id,
        protocol=mqtt.MQTTv311,
        callback_api_version=CallbackAPIVersion.VERSION2
    )
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, image_path):
    try:
        with open(image_path, 'rb') as file:
            filecontent = file.read()
            base64_content = base64.b64encode(filecontent)
            result = client.publish(topic, base64_content, qos=1, retain=True)
            msg_status = result[0]
            if msg_status != 0:
                print(f"❌ Failed to send message to topic '{topic}'")
            #else:
             #   print(f"📤 Published '{image_path}' to topic '{topic}'")
    except FileNotFoundError:
        print(f"🚫 Image file '{image_path}' not found.")

def main():
    client = connect_mqtt()
    client.loop_start()
    index = 0
    while True:
        publish(client, image_paths[index])
        index = 1 - index  # Toggle between 0 and 1
        time.sleep(1)  # Adjust this to control publish rate

main()
