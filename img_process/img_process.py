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
import platform
from PIL import Image
import matplotlib.pyplot as plt

from img_process.extract_names import clean_and_split_text, limpiar_array, obtener_posiciones_nombres


if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
elif platform.system() == "Linux":
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
else:
    raise OSError("Unsupported operating system")

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

    # Mostrar la imagen binarizada
    # plt.imshow(binary_img, cmap='gray')
    # plt.axis('off')
    # plt.show()

    return binary_img  # Devuelve la imagen binarizada

# Función para detectar las zonas de texto


def get_text_zones(img):
    """
    Detecta las zonas de la imagen donde se encuentra el texto y las almacena en un array.
    """
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    zones = []

    # Iterar sobre las palabras detectadas
    for i in range(len(data['text'])):
        if data['text'][i].strip():  # Si el texto no está vacío
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            zones.append({'text': data['text'][i], 'position': (x, y, w, h)})

    return zones

# Función para asociar texto limpio con zonas detectadas


def associate_text_with_zones_grid(band_array, image_size, padding=10):
    """
    Asocia cada banda con una zona en una cuadrícula de una imagen de tamaño 1:1.
    Devuelve una lista de objetos con la estructura {'name': 'nombre', 'band_id': '', 'img_zone': (x, y, width, height)}.
    """
    associations = []
    num_bands = len(band_array)

    # Calcular el tamaño de la cuadrícula
    grid_size = int(num_bands ** 0.5) + 1
    img_width, img_height, _ = image_size

    # Tamaño de cada celda de la cuadrícula
    cell_width = (img_width - padding * (grid_size + 1)) / grid_size
    cell_height = (img_height - padding * (grid_size + 1)) / grid_size

    # Crear una matriz para visualizar la cuadrícula
    grid_matrix = [['' for _ in range(grid_size)] for _ in range(grid_size)]

    # Asignar a cada banda una zona en la cuadrícula
    for i, band in enumerate(band_array):
        # Calcular la posición en la cuadrícula
        row = i // grid_size
        col = i % grid_size

        # Calcular las coordenadas de la zona
        x = col * cell_width + padding * (col + 1)
        y = row * cell_height + padding * (row + 1)

        # Ajustar el tamaño del puntero
        pointer_width = 120
        pointer_height = 40

        # Ajustar las coordenadas para el ratio 1:1
        adjusted_x = (x / img_width) * img_width
        adjusted_y = (y / img_height) * img_height

        # Ajustar el tamaño de la zona basado en el largo del nombre
        name_length = len(band['name'])
        zone_width = pointer_width + name_length * \
            5  # Ajuste basado en el largo del nombre
        zone_height = pointer_height

        # Asegurarse de que la zona no se salga de los límites de la imagen
        if adjusted_x + zone_width > img_width:
            adjusted_x = img_width - zone_width - padding
        if adjusted_y + zone_height > img_height:
            adjusted_y = img_height - zone_height - padding

        # Crear la asociación
        associations.append({
            'name': band['name'],
            'band_id': band.get('band_id', ''),
            'img_zone': (adjusted_x, adjusted_y, zone_width, zone_height)
        })

        # Actualizar la matriz de la cuadrícula
        grid_matrix[row][col] = band['name']

    # Imprimir la matriz de la cuadrícula
    for row in grid_matrix:
        print(row)

    return associations


# ----------------------------------------------------------------
# Seccion para actualziar y mejorar el analisis de texto
def extract_text_by_zones(image, zones):
    """
    Extrae texto de la imagen por las zonas especificadas.
    """
    extracted_texts = []

    for zone in zones:
        # Obtener las coordenadas de la zona
        x, y, w, h = zone['position']

        # Segmentar la imagen usando las coordenadas
        roi = image[y:y+h, x:x+w]  # Region of Interest

        # Usar Tesseract para extraer texto de la región
        text = pytesseract.image_to_string(roi)
        extracted_texts.append(text.strip())  # Agregar el texto extraído

    return extracted_texts


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
    print("\nTexto detectado:\n", texto)

    # Detectar zonas de texto
    text_zones = get_text_zones(clean_img_pil)
    # print("\nZonas de texto detectadas:\n", text_zones)

    # Limpias las zonas que no contienen texto
    band_zone = limpiar_array(text_zones)
    print("\nZonas de texto limpias:\n", band_zone)

    # Limpio y genero el array de objetos
    first_array_band = clean_and_split_text(texto)
    # valido que sea un array y imprimo su longitud
    print("first_array_bnand:", first_array_band)

    associated_data = obtener_posiciones_nombres(first_array_band, band_zone)
    print("\nTexto asociado a sus zonas:\n", associated_data)

    # # obtengo el image_size de la img subida
    # image_size = img_cv.shape

    # # Asociar el texto limpio con sus zonas
    # associated_data = associate_text_with_zones_grid(
    #     first_array_band, image_size)
    # # print("\nTexto asociado a sus zonas:\n", associated_data)

    # Retorna el texto detectado en formato JSON
    return associated_data
