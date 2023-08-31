
def colorizer(init_img_binary_data: bytes, params: dict):
    print(params["ckpt"])
    return 1111111111111111111111 #[init_img_binary_data]

def delete_background(init_img_binary_data: bytes, params: dict):
    return init_img_binary_data

def upscaler(init_img_binary_data: bytes, params: dict):
    return init_img_binary_data

def image_to_image(init_img_binary_data: bytes, caption: str, params: dict):
    return [init_img_binary_data, 1100011, 1110110111]

def text_to_image(caption: str, params: dict):
    return [1100011, 1110110111, 1100110111]

def image_captioning(init_img_binary_data: bytes, caption: str, params: dict):
    return 'fdgdfdfdddddddddghghgnhmhjmjjmjh'

def image_classification(init_img_binary_data: bytes):
    return [1, 2]

def translation(input_text: str, source_lang: str = "", dest_lang: str = "en"):
    return ("gggggg", "fgfghgfhgfhgfhfghgfh")

def inpainting(init_img_binary_data: bytes, mask_binary_data: bytes, caption: str, params: dict):
    return [init_img_binary_data, 111000010111, 1110001110]

def stylization(content_binary_data: bytes, style_binary_data: bytes, prompt: str, params: dict):
    return [1110001, 111000010111, 1110001110]

def image_fusion(img1_binary_data: bytes, img2_binary_data: bytes, prompt1: str, prompt2: str, params: dict):
    print(f'image_fusion{img1_binary_data},\t{img2_binary_data}')
    return [1110001, 111000010111, 1110001110]

  # nameNeuralTest = ['colorizer', 'delete_background', 'upscaler', 'image_to_image', 'text_to_image',
  #                     'image_captioning', 'translation', 'inpainting', 'stylization', 'image_fusion']
