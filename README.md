# OpenTTD Metrics Exporter

![Header image](https://github.com/sanjeyac/openttd-grafana-telemetry/blob/main/docs/header.jpg?raw=true)

## Introduction

This project is a fun and technical experiment:  
**Extracting real-time economic data from OpenTTD**, sending it to a **Python server**, exposing it as **Prometheus metrics**, and finally visualizing everything in **Grafana**!

The goal was to monitor **train economic performance** in real time, using only Open Source tools.

---

## Architecture

The system is built as follows:

1. **OpenTTD (custom modified)**  
   → Sends economic log data (e.g., train income, vehicle info) to a REST server.

2. **Python Server**  
   → Receives POST requests from OpenTTD and stores the latest vehicle data.  
   → Exposes metrics in Prometheus format at `/metrics`.

3. **Prometheus**  
   → Scrapes the Python server every few seconds.

4. **Grafana**  
   → Visualizes the train economics in real time with custom dashboards.

---

## How It Works

- OpenTTD was modified at the C++ level:  
  it sends a JSON payload every time a vehicle event occurs (example: when a train delivers cargo).

- The Python server:
  - Accepts incoming JSON via `POST /api/openttd/metrics`.
  - Stores only the **latest** data for each vehicle (no history).
  - Exposes metrics at `http://localhost:8080/metrics`.

- Prometheus scrapes these metrics every 5 seconds.

- Grafana pulls Prometheus data to generate dashboards showing company and vehicle performance.

---

## Project Components

- **Custom OpenTTD C++ Code**:
  - Modified to send JSON POST requests using `libcurl`.

- **Python Server** (no frameworks):
  - Basic HTTP server to receive and serve metrics.
  - No Flask, no FastAPI — just Python's `http.server` module.

- **Docker Compose** for Prometheus and Grafana:
  - Easy setup with shared volumes.
  - Prometheus configured to scrape the Python server.

---

## Setup Instructions

1. **Modify and Build OpenTTD**:
   - Clone OpenTTD sources.
   - Add C++ code to send POSTs on vehicle events.
   - Compile and run the custom binary.

2. **Run the Python server**:
   ```bash
   python3 server.py
      
3. Start Prometheus and Grafana with Docker Compose:
   ```bash
    docker-compose up -d

4. Create Grafana Dashboards:
    - Connect Grafana to Prometheus.
    - Create panels showing train revenues, company stats, etc.

## OpenTTD mod code

A little hook has been added in order to send a log event to grafana for each vehicle.

![Header image](https://github.com/sanjeyac/openttd-grafana-telemetry/blob/main/docs/vehicle_hook.png?raw=true)

A new logging function has been added to send data to grafana

![Header image](https://github.com/sanjeyac/openttd-grafana-telemetry/blob/main/docs/log.png?raw=true))


## Screenshots

(coming soon: dashboards screenshots!)

## License

This project is released under the MIT License.
