# Anomaly Detection in SaaS Access Data

This repository contains the code and resources for my Bachelor's Thesis project on anomaly detection in access data for SaaS (Software as a Service) applications. The goal of the project is to detect unusual patterns in user access logs, which may indicate security issues or abnormal behaviors, by using unsupervised machine learning techniques.

## Project Overview
The system is built around an ETL (Extract, Transform, Load) pipeline in **Python** that processes anonymized access data stored in a **PostgreSQL** database. This data is analyzed through machine learning models to identify potential anomalies. The project utilizes **Docker** for containerization, ensuring consistency across environments, and a **React** front-end interface for visualizing results.

## Features
- **Configurable ETL Pipeline**: The pipeline is managed through a YAML configuration file, allowing customization of database settings, data transformations, and model parameters.
- **Unsupervised Anomaly Detection**: Uses **Isolation Forest**, **DBSCAN**, and **Local Outlier Factor (LOF)** to detect unusual access patterns.
- **Data Visualization**: Generates visual representations of detected anomalies for easier interpretation.
- **Dockerized Deployment**: Encapsulates the application in Docker containers for improved portability and scalability.

## Technologies
- **Python**: Data processing and ETL pipeline development.
- **scikit-learn**: Clustering and outlier detection models.
- **PostgreSQL**: Database management for storing access data.
- **Docker**: Containerizes the application for consistent deployment.
- **React**: Front-end framework for visualizing results.
- **Flask**: Back-end API for data processing and integration with the front-end.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/cinodon/outlier-detection-saas-tfg.git
   cd tfg-iam-risk-pusture-poc
2. Set up and run Docker containers
   ```bash
   docker compose up
3. Access the app
   : http://localhost:3000

## Screenshots
![TFG_screenshot](https://github.com/user-attachments/assets/ca88a06a-bcae-4e94-8721-aa7f2d86ccf4)

## Demo
<details>
  <summary>▶ Click to watch the video</summary>

  <a href="https://youtu.be/S-yN3DxaOyw">
    <img src="https://img.youtube.com/vi/S-yN3DxaOyw/0.jpg" alt="Watch Video">
  </a>

</details>



### Handling Secrets and Network Configuration

This project includes secret files (such as database passwords) for full transparency, as it is a university project. Normally, these should be kept private, but in this case, they are accessible to everyone in the repository for evaluation purposes. Please handle them responsibly.

Additionally, the Flask backend communicates using a Docker socket. While this approach simplifies container networking and avoids additional service configuration, it is not recommended for production environments due to potential security risks. Exposing the Docker socket can lead to privilege escalation or unauthorized access to the host system. However, for this academic project, the risks have been evaluated, and the setup has been kept simple for demonstration purposes.

