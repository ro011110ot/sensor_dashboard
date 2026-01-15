# Climate Control Dashboard

A web-based monitoring system for climate data, integrating ESP32 nodes 
with a Flask backend and MariaDB storage.

## Architecture
- **Sensors (Indoor):** ESP32-S3 with DHT11 (Temperature & Humidity) running MicroPython.
- **Sensors (Outdoor):** ESP32 with DS18B20 (Temperature).
- **Database:** MariaDB (hosted on Debian 12 / HestiaCP).
- **Backend:** Flask (Python 3.11+) with `mysql-connector`.
- **Frontend:** Responsive Dark Mode UI using Bootstrap 5 and Chart.js.

## Installation with `uv`

Since this project uses `uv` for extremely fast and reliable Python package management:

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd sensor_dashboard
Create a virtual environment:

Bash

uv venv
Activate the environment:

Bash

source .venv/bin/activate
Install dependencies from requirements.txt:

Bash

uv pip install -r requirements.txt
Configuration: Ensure your .config file is present in the root directory with the following keys: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME.

Run the Dashboard:

Bash

./start_dash.sh
Database Synchronization
Measurements are synchronized to 15-minute intervals (:00, :15, :30, :45). The backend performs a fuzzy join across multiple tables to align indoor and outdoor data points even if timestamps vary by a few seconds.

Project Structure
app.py: Flask application with SQL grouping logic.

templates/index.html: Dashboard UI (Bootstrap & Chart.js).

requirements.txt: Python dependencies.

start_dash.sh: Startup script for the Flask development server.
