from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from PIL import Image

def aes_cbc_encrypt(data, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return iv + encrypted_data

def bytes_to_binary(byte_data):
    return ''.join(format(byte, '08b') for byte in byte_data)

def hide_data(image_path, data, key):
    encrypted_data = aes_cbc_encrypt(data, key)

    binary_data = bytes_to_binary(encrypted_data)
    binary_data += '1111111111111110'  # Adding a delimiter

    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    if len(binary_data) > width * height * 3:
        raise ValueError("Text too long to encode in the image")

    data_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))

            if data_index < len(binary_data):
                r = r & ~1 | int(binary_data[data_index])
                data_index += 1
            if data_index < len(binary_data):
                g = g & ~1 | int(binary_data[data_index])
                data_index += 1
            if data_index < len(binary_data):
                b = b & ~1 | int(binary_data[data_index])
                data_index += 1

            pixels[x, y] = (r, g, b)

    stego_image_path = "static/images/stego_image.png"
    img.save(stego_image_path)
    return stego_image_path
