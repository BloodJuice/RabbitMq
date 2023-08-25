#!/usr/bin/env python
import pika
import sys

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    nameNeuralTest = ['colorizer', 'delete_background', 'upscaler', 'image_to_image', 'text_to_image',
                      'image_captioning', 'translation', 'inpainting', 'stylization', 'image_fusion']

    for partOfMessage in nameNeuralTest:
        message = ' '.join(sys.argv[1:]) or "pic1 = 300 pic2 = 200 param = " + partOfMessage
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(f" [x] Sent {message}")
    connection.close()



main()