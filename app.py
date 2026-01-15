# app.py
from flask import Flask, render_template
import mysql.connector
from dotenv import dotenv_values
import os
from datetime import datetime

app = Flask(__name__)

script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, ".config")
CONFIG = dotenv_values(config_path)


def get_db_connection():
    return mysql.connector.connect(
        host=CONFIG.get("DB_HOST", "localhost"),
        user=CONFIG["DB_USER"],
        password=CONFIG["DB_PASSWORD"],
        database=CONFIG["DB_NAME"],
    )


@app.route("/")
def index():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # ... (Query bleibt gleich wie zuletzt besprochen) ...

    rows = []
    chart_data = []  # Zusätzliche Liste für JS
    try:
        cursor.execute(query)
        result = cursor.fetchall()

        # Wir drehen das Ergebnis für den Graphen um (älteste zuerst)
        for row in reversed(result):
            # String für JavaScript Graph (ISO Format)
            chart_row = row.copy()
            chart_row["time_label"] = row["time_slot"]
            chart_data.append(chart_row)

        # Liste für die Tabelle (neueste zuerst)
        for row in result:
            row["timestamp"] = datetime.strptime(row["time_slot"], "%Y-%m-%d %H:%M:%S")
            rows.append(row)

    except Exception as e:
        print(f"DATABASE ERROR: {e}")
    finally:
        cursor.close()
        db.close()

    return render_template("index.html", rows=rows, chart_data=chart_data)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Robust query: Rounds every timestamp to the nearest 15min slot BEFORE grouping
    query = """
    SELECT
        time_slot,
        MAX(IF(sensor='i_temp', value, NULL)) AS indoor_temp,
        MAX(IF(sensor='i_hum', value, NULL)) AS indoor_hum,
        MAX(IF(sensor='o_temp', value, NULL)) AS outdoor_temp
    FROM (
        SELECT
            DATE_FORMAT(timestamp - INTERVAL MINUTE(timestamp)%15 MINUTE,
                        '%Y-%m-%d %H:%i:00') as time_slot,
            'i_temp' as sensor, Temp as value
        FROM Sensors_Indoor_Temp
        UNION ALL
        SELECT
            DATE_FORMAT(timestamp - INTERVAL MINUTE(timestamp)%15 MINUTE,
                        '%Y-%m-%d %H:%i:00') as time_slot,
            'i_hum' as sensor, Humidity as value
        FROM Sensors_Indoor_Humidity
        UNION ALL
        SELECT
            DATE_FORMAT(timestamp - INTERVAL MINUTE(timestamp)%15 MINUTE,
                        '%Y-%m-%d %H:%i:00') as time_slot,
            'o_temp' as sensor, Temp as value
        FROM Sensors_Outdoor_DS18B20
    ) AS sub
    GROUP BY time_slot
    ORDER BY time_slot DESC
    LIMIT 40
    """

    rows = []
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print(f"DEBUG: Found {len(result)} rows in database.")  # Check your console!

        for row in result:
            # Convert string back to datetime for Jinja2 formatting
            row["timestamp"] = datetime.strptime(row["time_slot"], "%Y-%m-%d %H:%M:%S")
            rows.append(row)
    except Exception as e:
        print(f"DATABASE ERROR: {e}")
    finally:
        cursor.close()
        db.close()

    return render_template("index.html", rows=rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
