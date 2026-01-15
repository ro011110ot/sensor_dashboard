#!/bin/bash
source /home/ro011110ot/scripts/sensor_dashboard/.venv/bin/activate
exec gunicorn --workers 3 --bind unix:/tmp/sensor_dashboard.sock app:app
