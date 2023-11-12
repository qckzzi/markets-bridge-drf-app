import pika
from django.conf import (
    settings,
)


def publish(message: str, queue: str):
    with pika.BlockingConnection(pika.ConnectionParameters(**settings.AMQP_CONNECTION_PARAMETERS)) as connection:
        channel = connection.channel()
        channel.queue_declare(queue)
        channel.basic_publish(exchange='', routing_key=queue, body=message.encode())
