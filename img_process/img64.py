import base64
from PIL import Image
import io
import PIL
# img: <FileStorage: 'imageQ.jpg' ('image/jpeg')>

# Analizo e ltamano de la img y la reduzco a 256 kb

# Recivo la img abierta


def reduce_image_size(img_read):
    # Obtengo el tamaño de la imagen
    img = Image.open(io.BytesIO(img_read))
    # Obtengo cuánto kb pesa la imagen
    img_size = len(img_read) / 1024
    print("img_size", img_size)

    # Valido que la imagen sea menor a 256 kb
    while img_size > 256:
        # Reduzco el tamaño de la imagen
        img = img.resize((img.width // 2, img.height // 2),
                         Image.Resampling.LANCZOS)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_read = img_byte_arr.getvalue()
        img_size = len(img_read) / 1024
        print("img_size after resize", img_size)
    return img_read


def image_to_base64(image_file):
    img_read = image_file.read()
    # validar el tamano de la imagen
    img_read = reduce_image_size(img_read)

    if not img_read:
        return None

    # Convierte la imagen a base64
    base64_image = base64.b64encode(img_read).decode('utf-8')
    return base64_image
