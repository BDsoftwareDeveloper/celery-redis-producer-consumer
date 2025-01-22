# Dockerfile

# Use Python 3.8 as base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory
COPY app/ /app/

# Add /app to PYTHONPATH to ensure modules can be found
ENV PYTHONPATH=/app

# Set the default command to run Celery
CMD ["celery", "-A", "celeryconfig.app", "worker", "--loglevel=info"]
