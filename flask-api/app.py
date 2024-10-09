# flask-api/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS
import yaml
import os
import subprocess

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Ruta para obtener el archivo YAML
@app.route('/get-config', methods=['GET'])
def get_config():
    with open('/app/etl/etl_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return jsonify(config)


@app.route('/update-config', methods=['POST'])
def update_config():
    new_config = request.json

    # Parámetros que deben ser listas de floats y no permiten 'auto'
    float_params = ['max_samples', 'max_features', 'contamination', 'eps']

    # Parámetros que deben ser listas de ints
    int_params = ['n_estimators', 'min_samples', 'n_neighbors']

    # Convertir los parámetros de lista a los tipos apropiados
    for param in float_params:
        if param in new_config:
            values = new_config[param]
            if not isinstance(values, list):
                return jsonify({"error": f"{param} must be a list."}), 400
            for i, value in enumerate(values):
                try:
                    values[i] = float(value)
                except ValueError:
                    return jsonify({"error": f"Invalid value for {param}. Must be a float."}), 400
            new_config[param] = values

    for param in int_params:
        if param in new_config:
            values = new_config[param]
            if not isinstance(values, list):
                return jsonify({"error": f"{param} must be a list."}), 400
            for i, value in enumerate(values):
                try:
                    values[i] = int(value)
                except ValueError:
                    return jsonify({"error": f"Invalid value for {param}. Must be an int"}), 400
            new_config[param] = values

    config_path = '/app/etl/etl_config.yaml'
    with open(config_path, 'r') as file:
        current_config = yaml.safe_load(file)

    # Actualizar los parámetros con los nuevos valores
    for key, value in new_config.items():
        if key in current_config:
            current_config[key] = value

    with open(config_path, 'w') as file:
        yaml.dump(current_config, file)

    return jsonify({"message": "Configuration updated successfully", "updated_fields": new_config})


# Ruta para ejecutar el script ETL
@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Ejecutar el script y capturar la salida, con un timeout de 60 segundos
        result = subprocess.run(
            ["python3", "/app/etl/etl_script.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        # Devolver la salida estándar y la salida de error
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "message": "Execution completed successfully"
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            "error": "The script execution timed out. Please try again with different parameters."
        }), 504
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
