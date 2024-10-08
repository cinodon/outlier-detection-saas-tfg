FROM python:3.11-slim

# Crear directorios
RUN mkdir -p /app/etl/files/sql
RUN mkdir -p /app/etl/files/input
RUN mkdir -p /app/etl/files/output

# Copiar archivos SQL necesarios
COPY files/sql/query-raw-access-data.sql /app/etl/files/sql/
COPY files/sql/query-output-model-data.sql /app/etl/files/sql/

WORKDIR /app/etl

# Copiar el archivo de requerimientos e instalar dependencias
COPY etl-requirements.txt .
RUN pip install --no-cache-dir -r etl-requirements.txt

# Copiar el código fuente y el script de monitoreo
COPY . .
RUN chmod +x /app/etl/entrypoint.sh

# Ejecutar el script de monitoreo
CMD ["/app/etl/entrypoint.sh"]
