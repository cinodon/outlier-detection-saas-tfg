FROM python:3.11-slim

# Create directories
RUN mkdir -p /app/data_analysis/files/sql
RUN mkdir -p /app/data_analysis/files/input
RUN mkdir -p /app/data_analysis/files/output

# Copy SQL Queries
COPY files/sql/query-raw-access-data.sql /app/data_analysis/files/sql/
COPY files/sql/query-output-model-data.sql /app/data_analysis/files/sql/

WORKDIR /app/data_analysis

# Copy the script requirements and install dependencies
COPY data_analysis-requirements.txt .
RUN pip install --no-cache-dir -r data_analysis-requirements.txt

# Copy app
COPY . .

# Run script
CMD ["python", "/app/data_analysis/data_analysis_script.py"]
