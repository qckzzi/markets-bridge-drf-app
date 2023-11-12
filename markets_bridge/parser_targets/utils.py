from markets_bridge.amqp import (
    publish,
)


def publish_to_parsing_queue(message: str):
    publish(message, 'parsing')
