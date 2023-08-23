#!/usr/bin/env python
import pika
import time
# import INeural

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    print("dfgdfgdf")
    channel.start_consuming()


def callback(ch, method, properties, body):
    file, nameNeuralMethod = body.decode(), ''
    print(f" [x] Received {file}\n[x] Done")
    file = file.split()
    for step in range(len(file)):
        if file[step] == 'param':
            nameNeuralMethod = file[step + 2]
    # if nameNeuralMethod == 'colorizer':
    time.sleep(body.count(b'.'))

    ch.basic_ack(delivery_tag=method.delivery_tag)



main()