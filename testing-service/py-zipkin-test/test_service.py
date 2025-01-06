import pika
import requests
import time
import random

# RabbitMQ Configuration
RABBITMQ_HOST = 'rabbitmq.default.svc.cluster.local'
RABBITMQ_PORT = 5672
QUEUE_NAME = 'test_queue'

# Zipkin Configuration
ZIPKIN_URL = "http://zipkin.testing.svc.cluster.local:9411/api/v2/spans"

# Connect to RabbitMQ
def connect_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    return channel

# Send a message to RabbitMQ
def send_message(channel):
    message = f"Test message {random.randint(1, 100)}"
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
    print(f"Sent: {message}")

# Create a Zipkin trace span
def create_zipkin_span():
    trace = {
        "traceId": str(random.randint(1000000, 9999999)),
        "name": "send_message",
        "id": str(random.randint(1000000, 9999999)),
        "parentId": None,
        "annotations": [
            {"timestamp": int(time.time() * 1000), "value": "sr"},  # "sr" (server received)
            {"timestamp": int(time.time() * 1000 + 1000), "value": "ss"}  # "ss" (server sent)
        ],
        "tags": {
            "service": "test_service",
            "message": "sending_to_rabbitmq"
        }
    }
    requests.post(ZIPKIN_URL, json=[trace])
    print("Zipkin trace sent.")

# Main program
def main():
    channel = connect_rabbitmq()
    send_message(channel)
    create_zipkin_span()
    time.sleep(2)

if __name__ == "__main__":
    while True:
        main()
