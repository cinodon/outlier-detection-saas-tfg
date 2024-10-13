FROM python:3.11-slim

# Create directories
RUN mkdir -p /app/etl/files/sql
RUN mkdir -p /app/etl/files/input
RUN mkdir -p /app/etl/files/output

# Copy SQL Queries
COPY files/sql/query-raw-access-data.sql /app/etl/files/sql/
COPY files/sql/query-output-model-data.sql /app/etl/files/sql/

WORKDIR /app/etl

# Copy the script requirements and install dependencies
COPY etl-requirements.txt .
RUN pip install --no-cache-dir -r etl-requirements.txt

# Copy app
COPY . .

# Run script
CMD ["python", "/app/etl/etl_script.py"]
