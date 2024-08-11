# Light image for python11
FROM python:3.11-slim

# Crea el directorio /app/files
RUN mkdir -p /app/files

# Copiar el archivo SQL al directorio /files dentro del contenedor
COPY /files/query-raw-access-data.sql /files/

WORKDIR /app

# Copy requirements
COPY etl-requirements.txt .

# install all dependencies
RUN pip install --no-cache-dir -r etl-requirements.txt

# Copy code
COPY . .

# Run the script
CMD ["python", "etl_script.py"]