import pika
import requests
import time
import random
import os

# RabbitMQ Configuration
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq.testing.svc.cluster.local")
RABBITMQ_PORT = 5672
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "admin")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "secretpassword")
QUEUE_NAME = 'test_queue'

# Zipkin Configuration
ZIPKIN_URL = os.getenv("ZIPKIN_URL", "http://zipkin.testing.svc.cluster.local:9411/api/v2/spans")

# Connect to RabbitMQ
def connect_rabbitmq():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials,
        connection_attempts=5,
        retry_delay=2
    ))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    return channel

def main():
    try:
        channel = connect_rabbitmq()
        send_message(channel)
        create_zipkin_span()
        time.sleep(2)
    except pika.exceptions.AMQPConnectionError as e:
        print(f"RabbitMQ connection error: {e}")
        time.sleep(5)
