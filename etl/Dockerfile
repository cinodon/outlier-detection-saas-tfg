# Light image for python11
FROM python:3.11-slim

# Create directories
RUN mkdir -p /app/etl/files/sql
RUN mkdir -p /app/etl/files/input
RUN mkdir -p /app/etl/files/output

# Copy SQL
COPY files/sql/query-raw-access-data.sql /app/etl/files/sql/
COPY files/sql/query-output-model-data.sql /app/etl/files/sql/

WORKDIR /app/etl

# Copy requirements
COPY etl-requirements.txt .

# install all dependencies
RUN pip install --no-cache-dir -r etl-requirements.txt

# Copy code
COPY . .

# Run the script
CMD ["python", "etl_script.py"]