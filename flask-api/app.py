# flask-api/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS
import yaml
import docker


app = Flask(__name__)
CORS(app)  # Habilitar CORS

client = docker.from_env()

# Ruta para obtener el archivo YAML
@app.route('/get-config', methods=['GET'])
def get_config():
    with open('/app/etl/etl_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return jsonify(config)


@app.route('/update-config', methods=['POST'])
def update_config():
    try:
        new_config = request.json

        # Parámetros que deben ser listas de floats y no permiten 'auto' (excepto contamination)
        float_params = ['max_samples', 'max_features', 'eps']

        # Parámetros que deben ser listas de ints
        int_params = ['n_estimators', 'min_samples', 'n_neighbors']

        # Configuración especial para 'contamination' que permite 'auto'
        if 'contamination' in new_config:
            values = new_config['contamination']
            if not isinstance(values, list):
                return jsonify({"error": "contamination must be a list."}), 400
            for i, value in enumerate(values):
                if value == "auto":
                    values[i] = "auto"  # Permitir 'auto' sin cambios
                else:
                    try:
                        values[i] = float(value)  # Convertir a float si no es 'auto'
                    except ValueError:
                        return jsonify({"error": f"Invalid value for contamination. Must be 'auto' or a float."}), 400
            new_config['contamination'] = values

        # Procesar otros parámetros que deben ser floats
        for param in float_params:
            if param in new_config:
                values = new_config[param]
                if not isinstance(values, list):
                    return jsonify({f"error": f"{param} must be a list."}), 400
                for i, value in enumerate(values):
                    if value is not None:
                        try:
                            values[i] = float(value)
                        except ValueError:
                            return jsonify({"error": f"Invalid value for {param}. Must be a float."}), 400
                new_config[param] = [v for v in values if v is not None]

        # Procesar parámetros que deben ser ints
        for param in int_params:
            if param in new_config:
                values = new_config[param]
                if not isinstance(values, list):
                    return jsonify({"error": f"{param} must be a list."}), 400
                for i, value in enumerate(values):
                    if value is not None:
                        try:
                            values[i] = int(value)
                        except ValueError:
                            return jsonify({"error": f"Invalid value for {param}. Must be an int."}), 400
                new_config[param] = [v for v in values if v is not None]

        # Cargar y actualizar el YAML
        config_path = '/app/etl/etl_config.yaml'
        with open(config_path, 'r') as file:
            current_config = yaml.safe_load(file)

        for key, value in new_config.items():
            if key in current_config:
                current_config[key] = value

        with open(config_path, 'w') as file:
            yaml.dump(current_config, file)

        return jsonify({"message": "Configuration updated successfully", "updated_fields": new_config})

    except Exception as e:
        print("Error in update-config:", str(e))
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500


# Ruta para ejecutar el script ETL a través del contenedor Docker
@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        # Intentar obtener el contenedor ETL
        etl_container = client.containers.get("etl_service")

        # Si el contenedor existe pero está detenido, se inicia
        if etl_container.status == "exited":
            etl_container.start()
        elif etl_container.status == "running":
            # Si el contenedor está en ejecución, puede reiniciarse
            etl_container.restart()
        else:
            # En otros casos, se intenta eliminar y crear un nuevo contenedor
            etl_container.remove()
            etl_container = client.containers.run(
                "etl_image",  # Reemplaza esto con el nombre de la imagen ETL
                name="etl_service",
                detach=True,
                environment={
                    "DB_HOST": "db",
                    "DB_PASSWORD_FILE": "/run/secrets/db-password"
                },
                volumes={
                    './etl': {'bind': '/app/etl', 'mode': 'rw'}
                }
            )

        # Esperar a que el contenedor finalice
        etl_container.wait()

        # Obtener los logs de la salida del contenedor
        logs = etl_container.logs().decode("utf-8")

        return jsonify({"output": logs, "message": "Execution completed successfully"})

    except docker.errors.NotFound:
        # Si el contenedor no existe, crearlo y ejecutar el script
        etl_container = client.containers.run(
            "etl_image",  # Reemplaza con el nombre de la imagen ETL
            name="etl_service",
            detach=True,
            environment={
                "DB_HOST": "db",
                "DB_PASSWORD_FILE": "/run/secrets/db-password"
            },
            volumes={
                './etl': {'bind': '/app/etl', 'mode': 'rw'}
            }
        )

        # Esperar a que el contenedor finalice
        etl_container.wait()

        # Obtener los logs de la salida del contenedor
        logs = etl_container.logs().decode("utf-8")
        return jsonify({"output": logs, "message": "Execution completed successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
