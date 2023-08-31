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

    nameNeuralTest = ['colorizer', 'delete_background', 'upscaler', 'image_to_image', 'text_to_image',
                      'image_captioning', 'translation', 'inpainting', 'stylization', 'image_fusion']
    for i in nameNeuralTest:
        data = {
            "OrderId": "123e4567-e89b-12d3-a456-426655440000",
            # Тип нейронки
            "enum": i,
            # Параметры
            "params": {"ckpt": "ColorizeArtistic_gen", "steps": 1, "compare": False, "artistic": True, "render_factor": 12, "post_process": True, "clr_saturation_factor": 5, "line_color_limit": 100, "clr_saturate_every_step": True},
            # Изображения
            "init_img_binary_data": "4353534543dsfdsgsdgx///q//t",
            "img1_binary_data": "gththfyhy//dfthtfh5678899dfgfhtfhy656566776",
            "img2_binary_data": "gththfyhy//dfthtfh5678899dfdfvdfvfd11111111",
            "content_binary_data": "//dfthtfh5678899dfdfvdfvfd12121212121",
            # Описания
            "prompt": "zero_description",
            "prompt1": "first_description",
            "prompt2": "first_description",
            "caption": "caption_info",
            "mask_binary_data": "gththfyhy//xdfthtfh5678899dfdfvdfvfd00000",
            "style_binary_data": "Cool_Style",
            "input_text": "en",
            "source_lang": "en",
            "dest_lang": "en"
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