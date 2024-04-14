import pika
from django.conf import (
    settings,
)
from pika import BasicProperties


def publish(message: str, queue: str, headers: dict | None = None):
    with pika.BlockingConnection(pika.ConnectionParameters(**settings.AMQP_CONNECTION_PARAMETERS)) as connection:
        channel = connection.channel()
        channel.queue_declare(queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message.encode(),
            properties=BasicProperties(headers=headers),
        )
