# 🌡️ Climate Control Dashboard

A modern, high-performance monitoring system for climate data. This project integrates **ESP32 nodes** (running MicroPython) with a **Flask backend** and **MariaDB** storage to provide real-time insights into indoor and outdoor environments.

---

## 🏗️ Architecture & Stack

### 📱 Hardware Nodes
* **Indoor Station:** ESP32-S3 | MicroPython | DHT11 (Temp & Humidity)
* **Outdoor Station:** ESP32 | DS18B20 (Temperature)

### 🖥️ Server Side (Debian 12 / HestiaCP)
* **Backend:** Python 3.11+ | Flask Framework
* **Environment:** Managed via `uv` (Fast Python package installer)
* **Database:** MariaDB (Relational storage with optimized SQL views)
* **Web Server:** Integrated via HestiaCP / Nginx Proxy

### 📊 Frontend
* **UI:** Responsive Dark Edition (Bootstrap 5)
* **Visualization:** Chart.js for interactive climate history
* **Sync:** 15-minute slot synchronization logic

---

## 🚀 Installation with `uv`

We use **`uv`** for extremely fast and reliable dependency management.

### 1️⃣ Clone & Navigate
```bash
git clone git@github.com:ro011110ot/sensor_dashboard.git
cd sensor_dashboard
```

2️⃣ Environment Setup

```bash
# Create a virtual environment
uv venv

# Activate the environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

3️⃣ Configuration 🔧
Create a .config file in the root directory (this file is ignored by git):


```toml
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=sensor_db
```

4️⃣ Start Dashboard

```bash
chmod +x start_dash.sh
./start_dash.sh
```

⏱️ Database Synchronization
To ensure perfect alignment between different sensor types (DHT11 vs. DS18B20), the system uses a Time-Slot Sync logic:

Fixed Intervals: Measurements are triggered at :00, :15, :30, and :45 minutes.

Fuzzy Join: The SQL backend performs a time-grouping join using DATE_FORMAT. This ensures that even if timestamps vary by a few seconds between nodes, the indoor and outdoor data points appear in the same row in your dashboard.

📂 Project Structure

```Plaintext
.
├── app.py              # Flask backend & SQL Logic
├── .config             # Database credentials (local only)
├── requirements.txt    # Python dependencies
├── start_dash.sh       # Rapid deployment script
├── templates/
│   └── index.html      # Responsive Dark Mode Dashboard
└── README.md           # Documentation
```
