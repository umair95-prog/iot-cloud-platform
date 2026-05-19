from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import HTMLResponse
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import psycopg2

app = FastAPI()

# Store latest sensor value
latest_data = {
    "temperature": None,
    "timestamp": None
}

DB_CONFIG = {
    "host": "postgres",
    "database": "iotdb",
    "user": "iotuser",
    "password": "iotpassword",
    "port": 5432
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

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO sensor_data (temperature) VALUES (%s)",
        (data.temperature,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {
        "message": "Sensor data received and stored in PostgreSQL",
        "data": latest_data
    }

# GET endpoint
@app.get("/sensor-data")
def get_sensor_data():
    return latest_data

@app.get("/sensor-history")
def get_sensor_history():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, temperature, timestamp
        FROM sensor_data
        ORDER BY timestamp DESC
        LIMIT 10
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    history = [
        {
            "id": row[0],
            "temperature": row[1],
            "timestamp": row[2].isoformat()
        }
        for row in rows
    ]

    return history

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

    <h2>Live Temperature</h2>
    <p>Temperature: <span id="temperature">--</span> °C</p>
    <p id="timestamp">Waiting for data...</p>

    <h2>Latest 10 Stored Records</h2>
    <table border="1" cellpadding="8">
        <thead>
            <tr>
                <th>ID</th>
                <th>Temperature (°C)</th>
                <th>Timestamp</th>
            </tr>
        </thead>
        <tbody id="history-table">
            <tr>
                <td colspan="3">Waiting for history...</td>
            </tr>
        </tbody>
    </table>

    <script>
        async function fetchData() {
            const response = await fetch('/sensor-data');
            const data = await response.json();

            if (data.temperature !== null) {
                document.getElementById('temperature').innerText = data.temperature;
                document.getElementById('timestamp').innerText = 'Last update: ' + data.timestamp;
            }
        }

        async function fetchHistory() {
            const response = await fetch('/sensor-history');
            const history = await response.json();

            const tableBody = document.getElementById('history-table');
            tableBody.innerHTML = '';

            history.forEach(row => {
                const tr = document.createElement('tr');

                tr.innerHTML = `
                    <td>${row.id}</td>
                    <td>${row.temperature}</td>
                    <td>${row.timestamp}</td>
                `;

                tableBody.appendChild(tr);
            });
        }

        async function updateDashboard() {
            await fetchData();
            await fetchHistory();
        }

        setInterval(updateDashboard, 1000);
        updateDashboard();
    </script>
</body>
    </html>
    """