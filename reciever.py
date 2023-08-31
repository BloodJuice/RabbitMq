#!/usr/bin/env python
import json

import pika
import time
import Fake_Neural
import send


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
    data = json.loads(file)
    print(f" [x] Received {file}\n[x] Done")

    try:
        send.send(message=searchNeural(data))
    except Exception:
        print("\nYour type of Neural doesn't exist\n")

    time.sleep(body.count(b'.'))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def searchNeural(data):
    if data.get('enum') == 'colorizer':
        return str(Fake_Neural.colorizer(init_img_binary_data=data['pic1'], params=data['params']))
    elif data.get('enum') == 'delete_background':
        return str(Fake_Neural.delete_background(init_img_binary_data=data['pic1'], params=data['params']))
    elif data.get('enum') == 'upscaler':
        return str(Fake_Neural.upscaler(init_img_binary_data=data['pic1'], params=data['params']))
    elif data.get('enum') == 'image_to_image':
        return str(Fake_Neural.image_to_image(init_img_binary_data=data['pic1'], caption=data['caption'], params=data['params']))
    elif data.get('enum') == 'text_to_image':
        return str(Fake_Neural.text_to_image(caption='string', params=data['params']))
    elif data.get('enum') == 'image_captioning':
        return str(Fake_Neural.image_captioning(init_img_binary_data=data['pic1'], caption=data['caption'], params=data['params']))
    elif data.get('enum') == 'image_classification':
        return str(Fake_Neural.image_classification(init_img_binary_data=data['pic1']))
    elif data.get('enum') == 'translation':
        return str(Fake_Neural.translation(input_text=data['input_text'], source_lang=data['source_lang'], dest_lang=data['dest_lang']))
    elif data.get('enum') == 'inpainting':
        return str(Fake_Neural.inpainting(init_img_binary_data=data['pic1'], mask_binary_data=data['mask'], caption=data['caption'], params=data['params']))
    elif data.get('enum') == 'stylization':
        return str(Fake_Neural.stylization(content_binary_data=data['pic1'], style_binary_data=data['style'], prompt=data['prompt'], params=data['params']))
    elif data.get('enum') == 'image_fusion':
        return str(Fake_Neural.image_fusion(img1_binary_data=data['pic1'], img2_binary_data=data['pic2'], prompt1=data['prompt1'], prompt2=data['prompt2'], params=data['params']))


main()