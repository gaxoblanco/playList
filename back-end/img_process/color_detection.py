

import cv2
import numpy as np
from collections import Counter

# Función para detectar el color predominante


def get_dominant_color(img):
    """
    Calcula los dos colores predominantes de una imagen.
    Parámetros:
        img: array NumPy de la imagen (formato OpenCV)
    Retorna:
        List[Tuple (R, G, B)] de los dos colores predominantes
    """
    print("imgggg:", img)
    # Asegurarse de que la imagen tenga al menos 3 canales
    if img.shape[2] > 3:
        img = img[:, :, :3]

    resized_img = cv2.resize(
        img, (100, 100), interpolation=cv2.INTER_AREA)  # Reducir tamaño para optimizar
    pixels = resized_img.reshape(-1, 3)  # Convertir a una lista de píxeles
    most_common_colors = Counter(map(tuple, pixels)).most_common(
        2)  # Dos colores más frecuentes
    return [color[0] for color in most_common_colors]

# Función para calcular el color de contraste


def best_contrast_color(bg_colors):
    """
    Calcula el color que mejor contrasta con los dos colores de fondo.
    Parámetros:
        bg_colors: List[Tuple (R, G, B)] de los colores de fondo
    Retorna:
        Tuple (R, G, B) del color de texto sugerido
    """
    contrast_colors = []
    for bg_color in bg_colors:
        r, g, b = bg_color
        # Invertir el color
        contrast_color = (255 - r, 255 - g, 255 - b)
        contrast_colors.append(contrast_color)

    # Promediar los colores de contraste
    avg_contrast_color = tuple(np.mean(contrast_colors, axis=0).astype(int))
    # Convertir a tipos de datos nativos de Python
    avg_contrast_color = tuple(map(int, avg_contrast_color))
    # Convertir a formato hexadecimal
    hex_color = '#{:02x}{:02x}{:02x}'.format(
        avg_contrast_color[0], avg_contrast_color[1], avg_contrast_color[2])
    return hex_color
