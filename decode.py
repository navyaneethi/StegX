from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from PIL import Image

def aes_cbc_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
    return decrypted_data.decode("utf-8")

def bytes_from_image(image_path):
    img = Image.open(image_path)
    width, height = img.size
    binary_data = ""

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_data += bin(r)[-1] + bin(g)[-1] + bin(b)[-1]

    delimiter_pos = binary_data.find('1111111111111110')
    if delimiter_pos == -1:
        raise ValueError("Delimiter not found. No hidden message detected.")

    binary_data = binary_data[:delimiter_pos]
    byte_data = bytes([int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8)])
    return byte_data

def decode_data(image_path, key):
    byte_data = bytes_from_image(image_path)
    decrypted_message = aes_cbc_decrypt(byte_data, key)
    return decrypted_message