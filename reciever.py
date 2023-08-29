#!/usr/bin/env python
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
    data = dict()
    print(f" [x] Received {file}\n[x] Done")

    data = parseInputData(file=file.split())
    try:
        send.send(message=searchNeural(data))
    except Exception:
        print("\nYour type of Neural doesn't exist\n")

    time.sleep(body.count(b'.'))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def searchNeural(data):
    if data.get('param') == 'colorizer':
        return str(Fake_Neural.colorizer(init_img_binary_data=data.get('picOne'), params={'0': 1}))
    elif data.get('param') == 'delete_background':
        return str(Fake_Neural.delete_background(init_img_binary_data=data.get('picOne'), params={'0': 1}))
    elif data.get('param') == 'upscaler':
        return str(Fake_Neural.upscaler(init_img_binary_data=data.get('picOne'), params={'0': 1}))
    elif data.get('param') == 'image_to_image':
        return str(Fake_Neural.image_to_image(init_img_binary_data=data.get('picOne'), caption='string', params={'0': 1}))
    elif data.get('param') == 'text_to_image':
        return str(Fake_Neural.text_to_image(caption='string', params={'0': 1}))
    elif data.get('param') == 'image_captioning':
        return str(Fake_Neural.image_captioning(init_img_binary_data=data.get('picOne'), caption='string', params={'0': 1}))
    elif data.get('param') == 'image_classification':
        return str(Fake_Neural.image_classification(init_img_binary_data=data.get('picOne')))
    elif data.get('param') == 'translation':
        return str(Fake_Neural.translation(input_text='string', source_lang='string', dest_lang='string'))
    elif data.get('param') == 'inpainting':
        return str(Fake_Neural.inpainting(init_img_binary_data=data.get('picOne'), mask_binary_data=b'.', caption='string', params={'0': 1}))
    elif data.get('param') == 'stylization':
        return str(Fake_Neural.stylization(content_binary_data=data.get('picOne'), style_binary_data=b'.', prompt='string', params={'0': 1}))
    elif data.get('param') == 'image_fusion':
        return str(Fake_Neural.image_fusion(img1_binary_data=data.get('picOne'), img2_binary_data=data.get('picTwo'), prompt1='string', prompt2='string', params={'0': 1}))


# Функция разбиения исходной строки формата: "pic1 = byte pic2 = byte param = название нейронки"
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