# app/pubsub_tasks.py

# import random
# import time
# from celeryconfig import app
# import redis

# # Redis connection settings
# REDIS_HOST = 'redis'
# REDIS_PORT = 6379
# NUM_CHANNELS = 10

# @app.task
# def producer():
#     """Celery task that continuously produces messages to Redis channels."""
#     client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
#     message_count = 1

#     while True:  # Run indefinitely
#         # Determine the channel for this message in a round-robin manner
#         channel_number = (message_count - 1) % NUM_CHANNELS + 1
#         channel_name = f"channel_{channel_number}"
#         message = f"Real-time Message {message_count}"

#         # Publish the message to the appropriate channel
#         client.publish(channel_name, message)
#         print(f"[Producer] Published to {channel_name}: {message}")

#         message_count += 1
#         time.sleep(random.uniform(0.5, 2))  # Simulate delay between messages


# @app.task
# def consumer(channel_name):
#     """Celery task that subscribes to a Redis channel and processes messages."""
#     client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
#     pubsub = client.pubsub()
#     pubsub.subscribe(channel_name)
#     print(f"[Subscriber] Subscribed to {channel_name}. Waiting for messages...")

#     for message in pubsub.listen():
#         if message['type'] == 'message':  # Process only actual messages
#             print(f"[Subscriber] Received on {channel_name}: {message['data']}")
#             time.sleep(random.uniform(0.5, 1))  # Simulate processing time


import redis
from celery import shared_task

@shared_task
def producer(channel, message):
    """Celery task to publish messages to a Redis channel."""
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    r.publish(channel, message)
    print(f"Published: {message} on {channel}")

@shared_task
def consumer(channel):
    """Celery task to subscribe to a Redis channel and listen for messages."""
    r = redis.Redis(host='redis', port=6379, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    print(f"Subscribed to {channel}. Waiting for messages...")
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received: {message['data']} on {channel}")