from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import HTMLResponse
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

# Store latest sensor value
latest_data = {
    "temperature": None,
    "timestamp": None
}

temperature_gauge = Gauge(
    "iot_temperature_celsius",
    "Latest IoT sensor temperature in Celsius"
)

# Data model
class SensorData(BaseModel):
    temperature: float

# POST endpoint
@app.post("/sensor-data")
def receive_sensor_data(data: SensorData):

    latest_data["temperature"] = data.temperature
    latest_data["timestamp"] = datetime.now().isoformat()

    temperature_gauge.set(data.temperature)

    return {
        "message": "Sensor data received",
        "data": latest_data
    }

# GET endpoint
@app.get("/sensor-data")
def get_sensor_data():
    return latest_data


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <html>
    <head>
        <title>IoT Telemetry Dashboard</title>
    </head>
    <body>
        <h1>IoT Telemetry Dashboard</h1>
        <p>Temperature: <span id="temperature">--</span> °C</p>
        <p id="timestamp">Waiting for data...</p>

        <script>
            async function fetchData() {
                const response = await fetch('/sensor-data');
                const data = await response.json();

                if (data.temperature !== null) {
                    document.getElementById('temperature').innerText = data.temperature;
                    document.getElementById('timestamp').innerText = 'Last update: ' + data.timestamp;
                }
            }

            setInterval(fetchData, 1000);
            fetchData();
        </script>
    </body>
    </html>
    """