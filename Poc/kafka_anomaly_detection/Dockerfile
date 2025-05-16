# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# Ensure models directory is created
RUN mkdir -p /app/models

# Set Python path for modules
ENV PYTHONPATH="/app"

EXPOSE 5000
CMD ["python3", "main.py"]
