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
    channel.start_consuming()


def callback(ch, method, properties, body):
    file = body.decode()
    data = dict()
    print(f" [x] Received {file}\n[x] Done")
    print(f'parse:\t{parseInputData(file=file.split())}')

    time.sleep(body.count(b'.'))

    ch.basic_ack(delivery_tag=method.delivery_tag)

def parseInputData(file):
    data = dict()
    for step in range(len(file)):
        if file[step] == 'param':
            data['param'] = file[step + 2]
            i = 0
            while file[i] != 'param':
                if file[i] == 'pic1':
                    data['picOne'] = file[i + 2]
                elif file[i] == 'pic2':
                    data['picTwo'] = file[i + 2]
                i += 1
            break
    return data


main()