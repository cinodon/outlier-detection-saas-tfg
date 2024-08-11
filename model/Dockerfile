# Light image for python11
FROM python:3.11-slim

# Create directory /app/model files
RUN mkdir -p /app/model/files
RUN mkdir -p /app/model/output

WORKDIR /app/model

# Copy requirements
COPY model-requirements.txt .

# install all dependencies
RUN pip install --no-cache-dir -r model-requirements.txt

# Copy code
COPY . .

# Run the script
CMD ["python", "model.py"]