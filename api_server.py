from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Store latest sensor value
latest_data = {
    "temperature": None,
    "timestamp": None
}

# Data model
class SensorData(BaseModel):
    temperature: float

# POST endpoint
@app.post("/sensor-data")
def receive_sensor_data(data: SensorData):

    latest_data["temperature"] = data.temperature
    latest_data["timestamp"] = datetime.now().isoformat()

    return {
        "message": "Sensor data received",
        "data": latest_data
    }

# GET endpoint
@app.get("/sensor-data")
def get_sensor_data():
    return latest_data