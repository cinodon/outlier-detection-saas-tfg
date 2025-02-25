# flask-api/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import yaml
from celery_worker import run_data_analysis, celery
from celery.result import AsyncResult

# Create a Flask App
app = Flask(__name__)

# Enable CORS for React
CORS(app)

# Create docker client
client = docker.from_env()

# Get configuration YAML
@app.route('/get-config', methods=['GET'])
def get_config():
    with open('/app/data_analysis/data_analysis_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return jsonify(config)

# Update configuration YAML
@app.route('/update-config', methods=['POST'])
def update_config():
    try:
        # Get JSON from POST request
        new_config = request.json

        # Float parameters
        float_params = ['max_samples', 'max_features', 'eps']

        # Int parameters
        int_params = ['n_estimators', 'min_samples', 'n_neighbors']

        # Contamination
        # Check if it is modified
        if 'contamination' in new_config:
            values = new_config['contamination']
            # Check if it is a list
            if not isinstance(values, list):
                return jsonify({"error": "contamination must be a list."}), 400
            # If !auto try to transform it into a float
            for i, value in enumerate(values):
                if value == "auto":
                    values[i] = "auto"
                else:
                    try:
                        values[i] = float(value)
                    except ValueError:
                        return jsonify({"error": f"Invalid value for contamination. Must be 'auto' or a float."}), 400
            new_config['contamination'] = values

        # Transform float parameters
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

        # Transform int parameters
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

        # Load and update YAML
        config_path = '/app/data_analysis/data_analysis_config.yaml'
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

# Execute script running its docker service
@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        task = run_data_analysis.delay()  # Lanza la tarea en Celery
        return jsonify({"task_id": task.id, "message": "Task submitted"}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Task status
@app.route('/task-status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = AsyncResult(task_id, app=celery)
    if task.state in ['PENDING', 'STARTED']:
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.result,
            'status': task.result.get('message', '')
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info),
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
