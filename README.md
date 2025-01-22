# Project: Celery Redis Pub/Sub with Docker

## Project Structure
```
celery-redis-pubsub/
│
├── app/
│   ├── __init__.py          # Marks the directory as a Python package
│   ├── celeryconfig.py      # Celery configuration
│   ├── pubsub_tasks.py      # Producer and Consumer Celery tasks
│   └── requirements.txt     # Dependencies
│
├── Dockerfile               # Docker configuration for app
└── docker-compose.yml       # Docker Compose configuration for Redis and Celery worker
```

---

## Overview
This project demonstrates a real-time Pub/Sub messaging system using:
- **Redis**: For message brokering.
- **Celery**: For task management.
- **Docker**: To containerize the application for easy deployment and scaling.

---

## File Details

### 1. `app/__init__.py`
```python
# Empty file to mark the directory as a Python package
```

### 2. `app/celeryconfig.py`
```python
# app/celeryconfig.py

from celery import Celery

# Create the Celery app instance
app = Celery('pubsub_tasks', broker='redis://redis:6379/0')

# Celery configuration
app.conf.update(
    result_backend='redis://redis:6379/0',
)
```

### 3. `app/pubsub_tasks.py`
This file contains both the producer and consumer implementations as Celery tasks.

```python
import random
import time
from celeryconfig import app
import redis

# Redis connection settings
REDIS_HOST = 'redis'
REDIS_PORT = 6379
NUM_CHANNELS = 10

@app.task
def producer():
    """Celery task that continuously produces messages to Redis channels."""
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    message_count = 1

    while True:  # Run indefinitely
        # Determine the channel for this message in a round-robin manner
        channel_number = (message_count - 1) % NUM_CHANNELS + 1
        channel_name = f"channel_{channel_number}"
        message = f"Real-time Message {message_count}"

        # Publish the message to the appropriate channel
        client.publish(channel_name, message)
        print(f"[Producer] Published to {channel_name}: {message}")

        message_count += 1
        time.sleep(random.uniform(0.5, 2))  # Simulate delay between messages


@app.task
def consumer(channel_name):
    """Celery task that subscribes to a Redis channel and processes messages."""
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = client.pubsub()
    pubsub.subscribe(channel_name)
    print(f"[Subscriber] Subscribed to {channel_name}. Waiting for messages...")

    for message in pubsub.listen():
        if message['type'] == 'message':  # Process only actual messages
            print(f"[Subscriber] Received on {channel_name}: {message['data']}")
            time.sleep(random.uniform(0.5, 1))  # Simulate processing time



```

### 4. `app/requirements.txt`
```plaintext
redis
celery
```

### 5. `Dockerfile`
```Dockerfile
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
```

### 6. `docker-compose.yml`
```yaml
# docker-compose.yml

version: '3.8'

services:
  # Redis service
  redis:
    image: redis:alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - ./redis_data:/data

  # Celery worker service
  celery_worker:
    build: .
    container_name: celery_worker
    command: celery -A celeryconfig.app worker --loglevel=info
    depends_on:
      - redis
    environment:
      - CELERY_BROKER=redis://redis:6379/0

  # Producer (could be a separate service or just a task)
  producer:
    build: .
    container_name: celery_producer
    command: celery -A celeryconfig.app worker --loglevel=info
    depends_on:
      - redis

  # The default is to run Celery tasks, so there is no need for a web service

volumes:
  redis_data:
    driver: local
```

---

## Usage Instructions

### 1. Build and Start the Docker Containers
```bash
docker-compose up --build
```

### 2. Run the Producer Task
To publish messages to a channel:
```bash
docker-compose exec -it celery_worker bash
root@f5c5be665206:/app# python
>>> from pubsub_tasks import producer
>>> producer()


docker-compose exec celery_worker python -m pubsub_tasks producer channel_1
```

### 3. Run the Consumer Task
To consume messages from a channel:
```bash
docker-compose exec -it celery_worker bash
root@f5c5be665206:/app# python
>>> from pubsub_tasks import consumer
>>> consumer('channel_5')


docker-compose exec celery_worker python -m pubsub_tasks consumer channel_1
```

---

## Extending the Project
- Add more channels to handle different types of messages.
- Integrate logging for better traceability.
- Use Celery task scheduling for advanced message timing.
- Scale the worker instances using Docker Compose to handle higher loads.

---

This project is a starting point for building robust real-time messaging systems with Redis and Celery. Customize it to fit your specific use case!
