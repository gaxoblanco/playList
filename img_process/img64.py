import base64


def image_to_base64(image_path):
    # Abre la imagen en modo binario
    with open(image_path, "rb") as image_file:
        # Convierte la imagen a base64
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image
