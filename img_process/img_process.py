"""
URL para ejecutar en Google Colab
https://colab.research.google.com/drive/1FGmweUe0OwhugPHz9o5vxXF3dZc2DLG9#scrollTo=ina9caf2L3YV

---
tesseract-ocr + opencv
    Con una img procesada y en blanco y negro podemos usar un modelo mas economico
https://colab.research.google.com/drive/1cZrU05ua1Qm7BGkRQe9MJKDbvCdozF-7#scrollTo=0LJTaK-5j0Yk
"""
# pip install opencv-python-headless matplotlib pytesseract
# pip install pytesseract
# C:\Program Files\Tesseract-OCR

import cv2
import numpy as np
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt

from img_process.extract_names import clean_and_split_text


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Función para procesar la imagen (limpiar ruido y binarizar)


def preprocess_image(img):
    """
    Procesa la imagen para limpiarla (escala de grises, desenfoque y binarización).
    """
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro gaussiano para suavizar la imagen
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplicar binarización Otsu
    _, binary_img = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary_img  # Devuelve la imagen binarizada


def main(img):
    """
    Función principal para procesar la imagen.
    """
    # Lee la imagen desde el objeto FileStorage en un array de NumPy
    img_array = np.frombuffer(img.read(), np.uint8)
    img_cv = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Procesar la imagen
    clean_img = preprocess_image(img_cv)
    print("Imagen procesada con éxito")

    # Convertir la imagen procesada a formato PIL
    clean_img_pil = Image.fromarray(clean_img)

    # Usar Tesseract para extraer texto
    texto = pytesseract.image_to_string(clean_img_pil)

    # Mostrar el texto detectado
    print("\nTexto detectado:\n", texto)

    # Limpio y genero el array de objetos
    first_array_bnand = clean_and_split_text(texto)
    # valido que sea un array y imprimo su longitud
    # print("first_array_bnand:", first_array_bnand)
    print("len(first_array_bnand):", len(first_array_bnand))

    # Retorna el texto detectado en formato JSON
    return first_array_bnand
