import React, { useState } from 'react';
import './App.css'; // Importar el archivo de estilo

function App() {
  const [config, setConfig] = useState({
    run_if: false,
    n_estimators: '',
    max_samples: '',
    max_features: '',
    contamination: '',
    if_save_data: false,
    if_save_plot: false,
    run_dbscan: false,
    eps: '',
    min_samples: '',
    dbscan_save_data: false,
    dbscan_save_plot: false,
    run_lof: false,
    n_neighbors: '',
    lof_save_data: false,
    lof_save_plot: false
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setConfig((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const parseToList = (input, type) => {
    return input
      .split(',')
      .map((item) => {
        const trimmed = item.trim();
        if (trimmed === '') return null;
        if (type === 'float' && trimmed.toLowerCase() === 'auto') return "auto"; // Permitir 'auto' en contamination
        return type === 'int' ? parseInt(trimmed, 10) : parseFloat(trimmed);
      })
      .filter((item) => item !== null && (item === "auto" || !isNaN(item))); // Elimina null y NaN, permite 'auto'
  };

  const handleExecute = async () => {
  try {
    const configData = {};

    // Solo agregar a configData si hay valores
    if (config.n_estimators) configData.n_estimators = parseToList(config.n_estimators, 'int');
    if (config.max_samples) configData.max_samples = parseToList(config.max_samples, 'float');
    if (config.max_features) configData.max_features = parseToList(config.max_features, 'float');
    if (config.contamination) configData.contamination = parseToList(config.contamination, 'float');
    if (config.eps) configData.eps = parseToList(config.eps, 'float');
    if (config.min_samples) configData.min_samples = parseToList(config.min_samples, 'int');
    if (config.n_neighbors) configData.n_neighbors = parseToList(config.n_neighbors, 'int');

    // Solo incluir checkbox si están seleccionados o deseleccionados
    if (config.run_if !== '') configData.run_if = config.run_if;
    if (config.if_save_data !== '') configData.if_save_data = config.if_save_data;
    if (config.if_save_plot !== '') configData.if_save_plot = config.if_save_plot;
    if (config.run_dbscan !== '') configData.run_dbscan = config.run_dbscan;
    if (config.dbscan_save_data !== '') configData.dbscan_save_data = config.dbscan_save_data;
    if (config.dbscan_save_plot !== '') configData.dbscan_save_plot = config.dbscan_save_plot;
    if (config.run_lof !== '') configData.run_lof = config.run_lof;
    if (config.lof_save_data !== '') configData.lof_save_data = config.lof_save_data;
    if (config.lof_save_plot !== '') configData.lof_save_plot = config.lof_save_plot;

    // Enviar solo los campos que contienen valores al backend
    const response = await fetch('http://localhost:5000/update-config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(configData),
    });
    const result = await response.json();
    console.log(result);

    // Ejecutar el script después de actualizar la configuración
    await fetch('http://localhost:5000/run-script', {
      method: 'POST',
    });

  } catch (error) {
    console.error('Error updating config:', error);
  }
};


  return (
    <div className="app-container">
      <h1 className="title">Ejecución de algoritmos</h1>
      <p className="instructions">
        For each parameter, you can put its values as a single value or a list of values like a,b,c...
      </p>

      <div className="algorithm-section">
        <h2>Isolation Forest</h2>
        <div className="parameters">
          <label>Run Isolation Forest: <input type="checkbox" name="run_if" checked={config.run_if} onChange={handleChange} /></label>
          <label>n_estimators (range 100, 9999): <input type="text" name="n_estimators" value={config.n_estimators} onChange={handleChange} /></label>
          <label>max_samples (range 0.1, 1.0): <input type="text" name="max_samples" value={config.max_samples} onChange={handleChange} /></label>
          <label>max_features (range 0.1, 1.0): <input type="text" name="max_features" value={config.max_features} onChange={handleChange} /></label>
          <label>contamination (auto, range 0.01, 0.5): <input type="text" name="contamination" value={config.contamination} onChange={handleChange} /></label>
          <label>Save data: <input type="checkbox" name="if_save_data" checked={config.if_save_data} onChange={handleChange} /></label>
          <label>Save plot: <input type="checkbox" name="if_save_plot" checked={config.if_save_plot} onChange={handleChange} /></label>
        </div>
      </div>

      <div className="algorithm-section">
        <h2>DBSCAN</h2>
        <div className="parameters">
          <label>Run DBSCAN: <input type="checkbox" name="run_dbscan" checked={config.run_dbscan} onChange={handleChange} /></label>
          <label>eps (e.g., 0.5): <input type="text" name="eps" value={config.eps} onChange={handleChange} /></label>
          <label>min_samples (range 1, inf): <input type="text" name="min_samples" value={config.min_samples} onChange={handleChange} /></label>
          <label>Save data: <input type="checkbox" name="dbscan_save_data" checked={config.dbscan_save_data} onChange={handleChange} /></label>
          <label>Save plot: <input type="checkbox" name="dbscan_save_plot" checked={config.dbscan_save_plot} onChange={handleChange} /></label>
        </div>
      </div>

      <div className="algorithm-section">
        <h2>LOF</h2>
        <div className="parameters">
          <label>Run LOF: <input type="checkbox" name="run_lof" checked={config.run_lof} onChange={handleChange} /></label>
          <label>n_neighbors (range 1, n_samples): <input type="text" name="n_neighbors" value={config.n_neighbors} onChange={handleChange} /></label>
          <label>Save data: <input type="checkbox" name="lof_save_data" checked={config.lof_save_data} onChange={handleChange} /></label>
          <label>Save plot: <input type="checkbox" name="lof_save_plot" checked={config.lof_save_plot} onChange={handleChange} /></label>
        </div>
      </div>

      <button onClick={handleExecute}>Execute</button>
    </div>
  );
}

export default App;
