# flask-api/app.py

from flask import Flask, request, jsonify
import yaml
import subprocess
import os

app = Flask(__name__)

# Ruta para obtener el archivo YAML
@app.route('/get-config', methods=['GET'])
def get_config():
    with open('/app/etl/etl_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return jsonify(config)


# Ruta para actualizar un valor específico en el archivo YAML
@app.route('/update-config', methods=['POST'])
def update_config():
    new_config = request.json

    # Cargar el archivo YAML actual
    config_path = '/app/etl/etl_config.yaml'
    with open(config_path, 'r') as file:
        current_config = yaml.safe_load(file)

    # Actualizar solo las claves especificadas en la solicitud
    for key, value in new_config.items():
        if key in current_config:
            current_config[key] = value

    # Guardar el archivo YAML con las actualizaciones
    with open(config_path, 'w') as file:
        yaml.dump(current_config, file)

    return jsonify({"message": "Configuration updated successfully", "updated_fields": new_config})


# Ruta para ejecutar el script ETL
@app.route('/run-script', methods=['POST'])
def run_script():
    # Ejecutar el script ETL directamente en el contenedor `etl_service`
    result = subprocess.run(["docker", "exec", "etl_service", "python", "/app/etl/etl_script.py"],
                            capture_output=True, text=True)
    return jsonify({"stdout": result.stdout, "stderr": result.stderr})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
