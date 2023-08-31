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
        send.send(message=json.dumps(searchNeural(data)))
    except Exception:
        print("\nYour type of Neural doesn't exist\n")

    time.sleep(body.count(b'.'))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def searchNeural(data):
    result, saverLists = dict(), []
    if data.get('enum') == 'colorizer':
        result["picture"] = Fake_Neural.colorizer(init_img_binary_data=data['init_img_binary_data'], params=data['params'])
        return result
    elif data.get('enum') == 'delete_background':
        result["picture"] = Fake_Neural.delete_background(init_img_binary_data=data['init_img_binary_data'], params=data['params'])
        return result
    elif data.get('enum') == 'upscaler':
        result["picture"] = Fake_Neural.upscaler(init_img_binary_data=data['init_img_binary_data'], params=data['params'])
        return result
    elif data.get('enum') == 'image_to_image':
        saverLists = Fake_Neural.image_to_image(init_img_binary_data=data['init_img_binary_data'], caption=data['caption'], params=data['params'])
        return parserForList(saverLists)
    elif data.get('enum') == 'text_to_image':
        saverLists = Fake_Neural.text_to_image(caption=data['caption'], params=data['params'])
        return parserForList(saverLists)
    elif data.get('enum') == 'image_captioning':
        result["description"] = Fake_Neural.image_captioning(init_img_binary_data=data['init_img_binary_data'], caption=data['caption'], params=data['params'])
        return result
    elif data.get('enum') == 'image_classification':
        saverLists = Fake_Neural.image_classification(init_img_binary_data=data['init_img_binary_data'])
        return parserForList(saverLists)
    elif data.get('enum') == 'translation':
        return Fake_Neural.translation(input_text=data['input_text'], source_lang=data['source_lang'], dest_lang=data['dest_lang'])
    elif data.get('enum') == 'inpainting':
        saverLists = Fake_Neural.inpainting(init_img_binary_data=data['init_img_binary_data'], mask_binary_data=data['mask_binary_data'], caption=data['caption'], params=data['params'])
        return parserForList(saverLists)
    elif data.get('enum') == 'stylization':
        saverLists = Fake_Neural.stylization(content_binary_data=data['init_img_binary_data'], style_binary_data=data['style_binary_data'], prompt=data['prompt'], params=data['params'])
        return parserForList(saverLists)
    elif data.get('enum') == 'image_fusion':
        saverLists = Fake_Neural.image_fusion(img1_binary_data=data['img1_binary_data'], img2_binary_data=data['img2_binary_data'], prompt1=data['prompt1'], prompt2=data['prompt2'], params=data['params'])
        return parserForList(saverLists)

def parserForList(data):
    dictionary = dict()
    description = "img_binary_data_"
    for i in range(len(data)):
        dictionary[description + str(i)] = data[i]
    return dictionary

main()