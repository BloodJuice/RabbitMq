#!/usr/bin/env python
import json

import pika
import sys

def main():
    sendHard()
    # sendEasy()
def sendHard():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    data = {
        "OrderId": '123e4567-e89b-12d3-a456-426655440000',
        "params": {"ckpt": "ColorizeArtistic_gen", "steps": 1, "compare": False, "artistic": True, "render_factor": 12, "post_process": True, "clr_saturation_factor": 5, "line_color_limit": 100, "clr_saturate_every_step": True},
        "enum": 'colorizer',
        "pic1": 'gththfyhy//dfthtfh5678899dfgfhtfhy656566776'
    }

    message = json.dumps(data)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    print(f" [x] Sent {message}")
    connection.close()

def sendEasy():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)


    message = ' '.join(sys.argv[1:]) or "pic1 = 300 pic2 = 200 param = Hello,World!"
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