# app.py
from flask import Flask, render_template
import mysql.connector
from dotenv import dotenv_values
import os
from datetime import datetime

app = Flask(__name__)

# Configuration setup
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, ".config")
CONFIG = dotenv_values(config_path)

def get_db_connection():
    return mysql.connector.connect(
        host=CONFIG.get("DB_HOST", "localhost"),
        user=CONFIG["DB_USER"],
        password=CONFIG["DB_PASSWORD"],
        database=CONFIG["DB_NAME"]
    )

@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Diese Query gruppiert die Daten in 15-Minuten-Schritte
    # Die Formel FLOOR(MINUTE(timestamp)/15)*15 rundet die Minuten ab
    query = """
   SELECT
        CONCAT(DATE_FORMAT(timestamp, '%Y-%m-%d %H:'),
               LPAD(FLOOR(MINUTE(timestamp)/15)*15, 2, '0')) AS time_group,
        MAX(IF(sensor='i_temp', value, NULL)) AS indoor_temp,
        MAX(IF(sensor='i_hum', value, NULL)) AS indoor_hum,
        MAX(IF(sensor='o_temp', value, NULL)) AS outdoor_temp
    FROM (
        SELECT timestamp, 'i_temp' as sensor, Temp as value
        FROM Sensors_Indoor_Temp
        UNION ALL
        SELECT timestamp, 'i_hum' as sensor, Humidity as value
        FROM Sensors_Indoor_Humidity
        UNION ALL
        SELECT timestamp, 'o_temp' as sensor, Temp as value
        FROM Sensors_Outdoor_DS18B20
    ) AS sub
    GROUP BY time_group
    ORDER BY time_group DESC
    LIMIT 40
    """

    rows = []
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            # Wir wandeln den 'time_group' String in ein echtes datetime-Objekt um
            # Damit kann Jinja2 in der index.html .strftime() benutzen
            row['timestamp'] = datetime.strptime(row['time_group'], '%Y-%m-%d %H:%M')
            rows.append(row)
    except Exception as e:
        print(f"Error fetching data: {e}")
    finally:
        db.close()

    return render_template('index.html', sensor_data=rows)

if __name__ == '__main__':
    # Flask app is accessible on the network
    app.run(host='0.0.0.0', port=5000)
