import React, { useState } from 'react';
import './App.css'; // Importar el archivo de estilo

function App() {
  // Lógica de la aplicación

  return (
    <div className="app-container">
      <h1 className="title">Ejecución de algoritmos</h1>
      <p className="instructions">
        For each parameter, you can put its values as a single value or a list of values like a,b,c...
      </p>

      <div className="algorithm-section">
        <h2>Isolation Forest</h2>
        <div className="parameters">
          <label>Run Isolation Forest: <input type="checkbox" name="run_if" /></label>
          <label>n_estimators (range 100, 9999): <input type="text" name="n_estimators" /></label>
          <label>max_samples (range 0.1, 1.0): <input type="text" name="max_samples" /></label>
          <label>max_features (range 0.1, 1.0): <input type="text" name="max_features" /></label>
          <label>contamination (auto, range 0.01, 0.5): <input type="text" name="contamination" /></label>
          <label>Save data: <input type="checkbox" name="if_save_data" /></label>
          <label>Save plot: <input type="checkbox" name="if_save_plot" /></label>
        </div>
      </div>

      <div className="algorithm-section">
        <h2>DBSCAN</h2>
        <div className="parameters">
          <label>Run DBSCAN: <input type="checkbox" name="run_dbscan" /></label>
          <label>eps (e.g., 0.5): <input type="text" name="eps" /></label>
          <label>min_samples (range 1, inf): <input type="text" name="min_samples" /></label>
          <label>Save data: <input type="checkbox" name="dbscan_save_data" /></label>
          <label>Save plot: <input type="checkbox" name="dbscan_save_plot" /></label>
        </div>
      </div>

      <div className="algorithm-section">
        <h2>LOF</h2>
        <div className="parameters">
          <label>Run LOF: <input type="checkbox" name="run_lof" /></label>
          <label>n_neighbors (range 1, n_samples): <input type="text" name="n_neighbors" /></label>
          <label>Save data: <input type="checkbox" name="lof_save_data" /></label>
          <label>Save plot: <input type="checkbox" name="lof_save_plot" /></label>
        </div>
      </div>

      <button onClick={() => console.log("Executed")}>Execute</button>
    </div>
  );
}

export default App;
