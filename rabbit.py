import os
import pika

def get_connection():
    RABBIT_USER = os.getenv('RABBIT_USER', 'root')
    RABBIT_PASSWORD = os.getenv('RABBIT_USER', 'root')
    RABBIT_HOST = os.getenv('RABBIT_HOST', 'rabbitmq')
    RABBIT_PORT = os.getenv('RABBIT_PORT', '5672')
    RABBITMQ_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}/"
    return pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))

def get_channel(connection):
    return connection.channel()

def publish_message(channel, queue_name, message):
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
    )

def consume_messages(channel, queue_name, callback):
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming()
