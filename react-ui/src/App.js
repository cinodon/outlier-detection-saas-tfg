import React, { useState } from 'react';
import './App.css';

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
  //Script's output
  const [output, setOutput] = useState('');

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
        if (type === 'float' && trimmed.toLowerCase() === 'auto') return "auto";
        return type === 'int' ? parseInt(trimmed, 10) : parseFloat(trimmed);
      })
      .filter((item) => item !== null && (item === "auto" || !isNaN(item)));
  };

  const handleExecute = async () => {
    try {
      const configData = {};

      if (config.n_estimators) configData.n_estimators = parseToList(config.n_estimators, 'int');
      if (config.max_samples) configData.max_samples = parseToList(config.max_samples, 'float');
      if (config.max_features) configData.max_features = parseToList(config.max_features, 'float');
      if (config.contamination) configData.contamination = parseToList(config.contamination, 'float');
      if (config.eps) configData.eps = parseToList(config.eps, 'float');
      if (config.min_samples) configData.min_samples = parseToList(config.min_samples, 'int');
      if (config.n_neighbors) configData.n_neighbors = parseToList(config.n_neighbors, 'int');

      configData.run_if = config.run_if;
      configData.if_save_data = config.if_save_data;
      configData.if_save_plot = config.if_save_plot;
      configData.run_dbscan = config.run_dbscan;
      configData.dbscan_save_data = config.dbscan_save_data;
      configData.dbscan_save_plot = config.dbscan_save_plot;
      configData.run_lof = config.run_lof;
      configData.lof_save_data = config.lof_save_data;
      configData.lof_save_plot = config.lof_save_plot;

      // Update YAML calling update-config in Flask
      const updateResponse = await fetch('http://localhost:5000/update-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(configData),
      });
      await updateResponse.json();

      // Run script with Flask
      const executeResponse = await fetch('http://localhost:5000/run-script', {
        method: 'POST',
      });
      const result = await executeResponse.json();

      // Update the output
      setOutput(result.output || "No output from script");

    } catch (error) {
      console.error('Error executing script:', error);
      setOutput("Error executing script");
    }
  };

  return (
    <div className="app-container">
      <h1 className="title">Algorithm Execution</h1>
      <p className="instructions">
        For each parameter, you can put its values as a single value or a list of values like a,b,c...
      </p>

      <div className="main-content">
        <div className="algorithm-section-container">
          <div className="algorithm-section">
            <h2>Isolation Forest</h2>
            <div className="parameters">
              <label>Run Isolation Forest: <input type="checkbox" name="run_if" onChange={handleChange} /></label>
              <label>n_estimators (range 100, 9999): <input type="text" name="n_estimators" value={config.n_estimators} onChange={handleChange} /></label>
              <label>max_samples (range 0.1, 1.0): <input type="text" name="max_samples" value={config.max_samples} onChange={handleChange} /></label>
              <label>max_features (range 0.1, 1.0): <input type="text" name="max_features" value={config.max_features} onChange={handleChange} /></label>
              <label>contamination (auto, range 0.01, 0.5): <input type="text" name="contamination" value={config.contamination} onChange={handleChange} /></label>
              <label>Save data: <input type="checkbox" name="if_save_data" onChange={handleChange} /></label>
              <label>Save plot: <input type="checkbox" name="if_save_plot" onChange={handleChange} /></label>
            </div>
          </div>

          <div className="algorithm-section">
            <h2>DBSCAN</h2>
            <div className="parameters">
              <label>Run DBSCAN: <input type="checkbox" name="run_dbscan" onChange={handleChange} /></label>
              <label>eps (e.g., 0.5): <input type="text" name="eps" value={config.eps} onChange={handleChange} /></label>
              <label>min_samples (range 1, inf): <input type="text" name="min_samples" value={config.min_samples} onChange={handleChange} /></label>
              <label>Save data: <input type="checkbox" name="dbscan_save_data" onChange={handleChange} /></label>
              <label>Save plot: <input type="checkbox" name="dbscan_save_plot" onChange={handleChange} /></label>
            </div>
          </div>

          <div className="algorithm-section">
            <h2>LOF</h2>
            <div className="parameters">
              <label>Run LOF: <input type="checkbox" name="run_lof" onChange={handleChange} /></label>
              <label>n_neighbors (range 1, samples): <input type="text" name="n_neighbors" value={config.n_neighbors} onChange={handleChange} /></label>
              <label>Save data: <input type="checkbox" name="lof_save_data" onChange={handleChange} /></label>
              <label>Save plot: <input type="checkbox" name="lof_save_plot" onChange={handleChange} /></label>
            </div>
          </div>

          <button onClick={handleExecute}>Execute</button>
        </div>

        <div className="execution-output">
          <h2>Output</h2>
          <div className="output-box">
            <pre>{output}</pre> {/*Output*/}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
