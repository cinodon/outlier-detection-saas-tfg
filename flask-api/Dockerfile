# flask-api/Dockerfile

FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port 5000 (Flask)
EXPOSE 5000

# Run flask server
CMD ["python", "app.py"]
