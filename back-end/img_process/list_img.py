import os
from PIL import Image

# Buscar archivos .jpg en el directorio actual


def resize_image(image_path, max_size=(1024, 1024)):
    with Image.open(image_path) as img:
        img.thumbnail(max_size)
        return img


def listar_imagenes(directorio='.'):
    # Filtrar solo los archivos con extensión .jpg, .png, etc.
    imagenes = [f for f in os.listdir(
        directorio) if f.endswith(('.jpg', '.jpeg', '.png'))]

    if not imagenes:
        print("No se encontraron imágenes en el directorio.")
        return None

    # Mostrar las imágenes disponibles al usuario con numeración
    print("Imágenes disponibles en el directorio:")
    for idx, img in enumerate(imagenes, 1):
        print(f"{idx}. {img}")

    # Pedir al usuario que seleccione una imagen
    seleccion = input("Seleccione el número de la imagen que desea procesar: ")

    try:
        seleccion = int(seleccion) - 1  # Convertir la selección a índice
        if seleccion < 0 or seleccion >= len(imagenes):
            print("Selección inválida. Intente nuevamente.")
            return None
        else:
            imagen_seleccionada = imagenes[seleccion]
            print(f"Imagen seleccionada: {imagen_seleccionada}")
            return imagen_seleccionada
    except ValueError:
        print("Entrada no válida. Intente nuevamente.")
        return None
