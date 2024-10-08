#!/bin/bash
while true; do
    if [ -f "/app/etl/trigger_run.txt" ]; then
        echo "Trigger detected. Running ETL script..."
        python /app/etl/etl_script.py
        echo "Script executed. Removing trigger."
        rm /app/etl/trigger_run.txt
    fi
    sleep 5  # Esperar 5 segundos antes de verificar nuevamente
done
