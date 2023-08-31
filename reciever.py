#!/usr/bin/env python
import json
import pika
import time
import INeural
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

# Функция вызова методов из файла Антона с нейронками
def searchNeural(data):
    result, saverLists = dict(), []
    if data['enum'] == 'colorizer':
        result["picture"] = INeural.colorizer(init_img_binary_data=data['init_img_binary_data'], params=data['params'])
        return result
    elif data['enum'] == 'delete_background':
        result["picture"] = INeural.delete_background(init_img_binary_data=data['init_img_binary_data'], params=data['params'])
        return result
    elif data['enum'] == 'upscaler':
        result["picture"] = INeural.upscaler(init_img_binary_data=data['init_img_binary_data'], params=data['params'])
        return result
    elif data['enum'] == 'image_to_image':
        saverLists = INeural.image_to_image(init_img_binary_data=data['init_img_binary_data'], caption=data['caption'], params=data['params'])
        return parserForList(saverLists)
    elif data['enum'] == 'text_to_image':
        saverLists = INeural.text_to_image(caption=data['caption'], params=data['params'])
        return parserForList(saverLists)
    elif data['enum'] == 'image_captioning':
        result["description"] = INeural.image_captioning(init_img_binary_data=data['init_img_binary_data'], caption=data['caption'], params=data['params'])
        return result
    elif data['enum'] == 'image_classification':
        saverLists = INeural.image_classification(init_img_binary_data=data['init_img_binary_data'])
        return parserForList(saverLists)
    elif data['enum'] == 'translation':
        return INeural.translation(input_text=data['input_text'], source_lang=data['source_lang'], dest_lang=data['dest_lang'])
    elif data['enum'] == 'inpainting':
        saverLists = INeural.inpainting(init_img_binary_data=data['init_img_binary_data'], mask_binary_data=data['mask_binary_data'], caption=data['caption'], params=data['params'])
        return parserForList(saverLists)
    elif data['enum'] == 'stylization':
        saverLists = INeural.stylization(content_binary_data=data['init_img_binary_data'], style_binary_data=data['style_binary_data'], prompt=data['prompt'], params=data['params'])
        return parserForList(saverLists)
    elif data['enum'] == 'image_fusion':
        saverLists = INeural.image_fusion(img1_binary_data=data['img1_binary_data'], img2_binary_data=data['img2_binary_data'], prompt1=data['prompt1'], prompt2=data['prompt2'], params=data['params'])
        return parserForList(saverLists)

# Функция для парсинга получаемых списков из методов Антона. Необходима для составления из них словаря.
def parserForList(data):
    dictionary = dict()
    description = "img_binary_data_"
    for i in range(len(data)):
        dictionary[description + str(i)] = data[i]
    return dictionary

main()