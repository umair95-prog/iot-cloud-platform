# IoT Cloud Platform

A real-time IoT telemetry and monitoring platform built with Python, AWS IoT Core, MQTT, FastAPI, and a live web dashboard.

This project demonstrates an end-to-end data flow from a simulated IoT device to cloud ingestion, backend API communication, and real-time visualization.

---

## Project Overview

The system simulates sensor telemetry data and publishes it through MQTT to AWS IoT Core. The same telemetry is forwarded to a FastAPI backend through REST endpoints, where the latest sensor values are exposed to a live dashboard.

---



## System Architecture

```mermaid
flowchart TD
    A[Simulated IoT Device<br>Python MQTT Publisher] -->|MQTT Telemetry| B[AWS IoT Core]

    A -->|HTTP POST /sensor-data| C[FastAPI REST Backend]

    C -->|Expose latest telemetry| D[Live Web Dashboard]

    C -->|Expose /metrics endpoint| E[Prometheus]

    E -->|Scraped telemetry metrics| F[Grafana Dashboard]

    G[Docker Compose] --> C
    G --> E
    G --> F

    H[Kubernetes Deployment] --> C
    I[Kubernetes Service<br>NodePort 30080] --> H
```

## AWS-Native Serverless Pipeline

The project also includes an AWS-native telemetry flow using AWS IoT Core, IoT Rules, Lambda, and Amazon S3.

### AWS Serverless Architecture

```mermaid
flowchart TD
    A[Simulated IoT Device<br>Python MQTT Publisher]
        -->|MQTT Telemetry| B[AWS IoT Core]

    B -->|IoT Rule<br>SELECT * FROM 'sensor/data'| C[AWS Lambda]

    C -->|Store JSON telemetry| D[Amazon S3<br>iot-data/]
```

### Components

- **AWS IoT Core** receives MQTT telemetry from the simulated device
- **IoT Rule Engine** routes messages from the `sensor/data` topic
- **AWS Lambda** processes incoming telemetry events
- **Amazon S3** stores telemetry payloads as JSON files under `iot-data/`
- The MQTT publisher supports AWS-only mode using `ENABLE_LOCAL_API = False`

### Runtime Modes

The MQTT publisher can run in two modes:

```python
ENABLE_LOCAL_API = False
```

AWS-native mode:

```text
MQTT Publisher → AWS IoT Core → IoT Rule → Lambda → S3
```

```python
ENABLE_LOCAL_API = True
```

Hybrid local monitoring mode:

```text
MQTT Publisher → AWS IoT Core + Local FastAPI Dashboard
```

## Features

- Real-time sensor telemetry simulation
- MQTT publish/subscribe communication
- Secure AWS IoT Core connection using device certificates
- FastAPI-based REST API for telemetry ingestion
- JSON-based HTTP communication
- Live browser dashboard with automatic data updates
- Git-based project version control

---

## Technologies Used

- Python
- AWS IoT Core
- MQTT
- FastAPI
- REST API
- JSON
- HTML / JavaScript
- Git
- Linux / CLI workflow

---

## API Endpoints

### POST `/sensor-data`

Receives sensor telemetry data.

Example request:

```json
{
  "temperature": 27.5
}
```

---

### GET `/sensor-data`

Returns the latest telemetry value.

Example response:

```json
{
  "temperature": 27.5,
  "timestamp": "2026-05-13T14:30:22"
}
```

---

## Running the Project Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Start FastAPI server

```bash
uvicorn api_server:app --reload
```

Open:

```text
http://127.0.0.1:8000/
```

---

### 3. Start MQTT publisher

In a second terminal:

```bash
python mqtt_publish.py
```

---

## Security Note

AWS certificates and private keys are not included in this repository. They are excluded using `.gitignore`.

---

## Docker Support

The FastAPI backend can also be run inside a Docker container.

### Build Docker image

```bash
docker build -t iot-fastapi-backend .
```

### Run Docker container

```bash
docker run -p 8000:8000 iot-fastapi-backend
```

Open:

```text
http://127.0.0.1:8000/
```

The dashboard and API will run from inside the containerized environment.


---

## Kubernetes Deployment

The FastAPI backend can also be deployed locally using Kubernetes through Docker Desktop.

### Apply Kubernetes configuration

```bash
kubectl apply -f k8s/
```

### Check running pods

```bash
kubectl get pods
```

### Check service

```bash
kubectl get services
```

### Access the application

```text
http://localhost:30080/
```

### Stop Kubernetes deployment

```bash
kubectl delete -f k8s/
```

This deployment uses a Kubernetes `Deployment` to run the FastAPI container and a `NodePort` service to expose it locally.




## Monitoring Stack

The platform includes a containerized monitoring and observability stack using Prometheus and Grafana.

### Monitoring Architecture

```text
IoT Device Simulation
        ↓
FastAPI Backend
        ↓
Prometheus Metrics Endpoint (/metrics)
        ↓
Prometheus Scraping
        ↓
Grafana Dashboard Visualization
```

### Monitoring Components

- Prometheus used for telemetry metric collection and scraping
- Grafana used for real-time dashboard visualization
- Custom temperature metrics exported from FastAPI using Prometheus client library
- Docker Compose used for multi-service orchestration

### Running the Monitoring Stack

```bash
docker compose up --build
```

### Access Services

FastAPI Dashboard:

```text
http://127.0.0.1:8000/
```

Prometheus:

```text
http://127.0.0.1:9090/
```

Grafana:

```text
http://127.0.0.1:3000/
```

Default Grafana credentials:

```text
Username: admin
Password: admin
```


---

## Project Screenshots

### Grafana Monitoring Dashboard

![Grafana Dashboard](screenshots/grafana-dashboard.png)

---

### FastAPI Live Telemetry Dashboard

![FastAPI Dashboard](screenshots/fastapi-dashboard.png)

---

### Prometheus Metrics Monitoring

![Prometheus Metrics](screenshots/prometheus-metrics.png)

---

### Docker Containerized Services

![Docker Containers](screenshots/docker-containers.png)


---

### Kubernetes Deployment

![Kubernetes Deployment](screenshots/kubernetes-deployment.png)

## Current Status

The platform currently includes:

- Real-time MQTT telemetry publishing using AWS IoT Core
- FastAPI-based REST API backend for telemetry ingestion
- Live browser dashboard for telemetry visualization
- Dockerized backend deployment workflows
- Prometheus-based metrics scraping and monitoring
- Grafana dashboard integration for real-time observability
- Docker Compose orchestration for multi-service deployment
- Git-based version control and feature branch workflow

Planned future extensions include:

- Kubernetes-based container orchestration
- Advanced Grafana dashboards and alerting
- Persistent telemetry storage and historical analytics
- Cloud-native deployment and scaling workflows