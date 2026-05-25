from awscrt import io, mqtt
from awsiot import mqtt_connection_builder
import json
import time
import random
from datetime import datetime
import requests

# =========================
# 1. AWS IoT Core Endpoint
# =========================
# Replace this with your actual endpoint from AWS IoT Core settings
endpoint = "aj120mlle7cja-ats.iot.eu-north-1.amazonaws.com"

# =========================
# 2. Certificate file paths
# =========================
cert_path = "certs/device.pem.crt"
key_path = "certs/private.pem.key"
root_ca_path = "certs/AmazonRootCA1.pem"

# =========================
# 3. MQTT settings
# =========================
client_id = "my-iot-device"
topic = "sensor/data"

# =========================
# 4. Runtime configuration
# =========================
ENABLE_LOCAL_API = True

# =========================
# 5. Create MQTT connection
# =========================
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=endpoint,
    cert_filepath=cert_path,
    pri_key_filepath=key_path,
    ca_filepath=root_ca_path,
    client_id=client_id,
    clean_session=False,
    keep_alive_secs=30,
)

print("Connecting to AWS IoT Core...")

# Connect
connect_future = mqtt_connection.connect()
connect_future.result()

print("Connected successfully!")

# =========================
# 6. Publish loop (simulated sensor)
# =========================
while True:
    data = {
        "temperature": round(random.uniform(20, 35), 2),
        "timestamp": str(datetime.now())
    }

    message = json.dumps(data)

    mqtt_connection.publish(
        topic=topic,
        payload=message,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )

    print("Published MQTT:", message)

    if ENABLE_LOCAL_API:
        response = requests.post(
 #          "http://127.0.0.1:8000/sensor-data",
            "http://16.171.166.0:8000/sensor-data",
            json={"temperature": data["temperature"]}
        )

#       print("Sent to FastAPI:", response.status_code, response.json())
        print("Sent to FastAPI:", response.status_code)
        print("Response text:", response.text)

    time.sleep(3)