"""
 Ejemplo de uso:
 -----------------
# 1. Cargar y preprocesar imagen
 img = cv2.imread("cartel.jpg")
 clean_img = preprocess_image(img)
 
# 2. Procesar para obtener bandas con posiciones
 bands = process_bands(clean_img)
 
# 3. Imprimir resultados
 for band in bands:
     print(f"Banda: {band['name']}")
     print(f"Posición: {band['img_zone']}")
     print("-" * 30)

"""
# pip install opencv-python-headless matplotlib pytesseract
# pip install pytesseract
# C:\Program Files\Tesseract-OCR
import json
import re
import base64
import cv2
import numpy as np
import pytesseract
import platform
from img_process.color_detection import get_dominant_color, best_contrast_color
from img_process.service.img_clear_process import preprocess_image
from img_process.service.text_zone import get_text_zones
from img_process.service.text_names import extract_band_names
from img_process.service.find_band_positions import find_band_positions

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
elif platform.system() == "Linux":
    pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
else:
    raise OSError("Unsupported operating system")


def process_bands(img):
    """
    Función principal que integra todo el proceso.
    Recibe una imagen preprocesada y devuelve las bandas con sus posiciones.
    """
    # Extraer texto completo
    full_text = pytesseract.image_to_string(img)
    print("\nTexto detectado:\n", full_text)

    # Obtener zonas de texto
    text_zones = get_text_zones(img)
    print("\nZonas de texto detectadas:", len(text_zones))

    # Extraer nombres de bandas
    band_names = extract_band_names(full_text)
    print("\nBandas extraídas:", len(band_names))

    # Asociar nombres con posiciones
    result = find_band_positions(band_names, text_zones)
    print("\nBandas con posiciones:", len(result))

    return result


def img_process(img64):
    """
    Función principal para procesar la imagen.
    """
    # Verifica si la cadena tiene el prefijo correcto
    if ',' in img64:
        # Decodifica la parte Base64
        img_data = base64.b64decode(img64.split(',')[1])
    else:
        raise ValueError(
            "El formato de la imagen no es válido. No se encontró el prefijo esperado.")
    # Decodifico la imagen base64
    img = np.frombuffer(img_data, np.uint8)
    img_cv = cv2.imdecode(img, cv2.IMREAD_COLOR)

    # Procesar la imagen
    clean_img = preprocess_image(img_cv)
    print("Imagen procesada con éxito")

    # 2. Procesar para obtener bandas con posiciones
    bands = process_bands(clean_img)
    print(f'Bandas procesadas: {len(bands)}')
    print(bands)

    # valido que tenemos una lista de string, si no es asi devuelvo un mensaje de error 202, la img no contiene nombre de bandas
    if not isinstance(bands, list) or len(bands) == 0:
        return {"error": 202, "message": "La imagen no contiene nombres de bandas detectables"}

    # Detectar color predominante
    dominant_color = get_dominant_color(img_cv)
    print("Color predominante (fondo):\n")

    # Calcular color de contraste
    contrast_color = best_contrast_color(dominant_color)
    print("Color sugerido para texto:\n")

    # Preparar respuesta final en JSON
    result = {
        "associated_data": bands,
        # "dominant_color": dominant_color,
        "contrast_color": contrast_color  # Convert set to list
    }
    # print("\nRespuesta final:\n", result)

    return result
