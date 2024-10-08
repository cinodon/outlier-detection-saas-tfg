# flask-api/Dockerfile

FROM python:3.11-slim

# Crear el directorio de la app
WORKDIR /app

# Copiar y instalar requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Expone el puerto de Flask
EXPOSE 5000

# Ejecutar el servidor Flask
CMD ["python", "app.py"]
