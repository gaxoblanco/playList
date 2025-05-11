import base64
from PIL import Image
import io
import os
import re


def reduce_image_size(img_data):
    """
    Reduce el tamaño de una imagen para cumplir con los requisitos de Spotify.

    Args:
        img_data: Bytes de la imagen

    Returns:
        bytes: Imagen procesada en formato JPEG
    """
    try:
        # Abrir la imagen desde los bytes
        img = Image.open(io.BytesIO(img_data))

        # Convertir a RGB si es necesario
        if img.mode != 'RGB':
            print(f"Convirtiendo imagen de formato {img.mode} a RGB")
            img = img.convert('RGB')

        # Obtener dimensiones originales
        width, height = img.size
        print(f"Dimensiones originales: {width}x{height}")

        # Hacer cuadrada la imagen recortando desde el centro si es necesario
        if width != height:
            print("La imagen no es cuadrada, recortando a proporción 1:1")
            square_size = min(width, height)
            left = (width - square_size) // 2
            top = (height - square_size) // 2
            right = left + square_size
            bottom = top + square_size
            img = img.crop((left, top, right, bottom))
            width, height = img.size
            print(f"Después de recortar: {width}x{height}")

        # Reducir dimensiones si es necesario (Spotify recomienda 300x300 como mínimo)
        target_size = 300
        if width < target_size or height < target_size:
            # Si la imagen es más pequeña, aumentarla a 300x300
            print(f"Imagen pequeña, aumentando a {target_size}x{target_size}")
            img = img.resize((target_size, target_size),
                             Image.Resampling.LANCZOS)
        elif width > 650 or height > 650:
            # Si es muy grande, reducirla a tamaño óptimo
            print(f"Imagen grande, reduciendo")
            img = img.resize((target_size, target_size),
                             Image.Resampling.LANCZOS)

        # Aplicar compresión JPEG con calidad media-alta
        quality = 85
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=quality, optimize=True)
        img_byte_arr.seek(0)
        img_data = img_byte_arr.getvalue()
        img_size = len(img_data) / 1024  # Tamaño en KB

        print(f"Tamaño inicial con calidad {quality}: {img_size:.2f} KB")

        # Si es mayor a 256 KB, intentar reducir la calidad gradualmente
        if img_size > 256:
            print("Reduciendo calidad para cumplir con límite de tamaño...")
            for quality in [70, 55, 40, 30, 20, 10]:
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG',
                         quality=quality, optimize=True)
                img_byte_arr.seek(0)
                img_data = img_byte_arr.getvalue()
                img_size = len(img_data) / 1024
                print(f"Calidad {quality}: {img_size:.2f} KB")

                if img_size <= 256:
                    print(f"Calidad óptima encontrada: {quality}")
                    break

        # Si aún es demasiado grande, reducir tamaño
        if img_size > 256:
            for size in [250, 200]:
                print(f"Reduciendo dimensiones a {size}x{size}")
                img = img.resize((size, size), Image.Resampling.LANCZOS)
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG',
                         quality=quality, optimize=True)
                img_byte_arr.seek(0)
                img_data = img_byte_arr.getvalue()
                img_size = len(img_data) / 1024
                print(f"Tamaño después de reducir: {img_size:.2f} KB")

                if img_size <= 256:
                    break

        # Calcular tamaño base64
        base64_size = len(base64.b64encode(img_data)) / 1024
        print(
            f"Tamaño final imagen: {img_size:.2f} KB, Base64: {base64_size:.2f} KB")

        return img_data

    except Exception as e:
        print(f"Error procesando imagen: {e}")
        import traceback
        traceback.print_exc()
        return None


def is_base64(s):
    """
    Comprueba si una cadena es una representación válida en base64.

    Args:
        s: Cadena a comprobar

    Returns:
        bool: True si es una cadena base64 válida
    """
    try:
        # Patrón para cadenas base64 (puede tener padding = al final)
        pattern = r'^[A-Za-z0-9+/]+={0,2}$'
        if not re.match(pattern, s):
            return False

        # Intentar decodificar
        base64.b64decode(s)
        return True
    except Exception:
        return False


def image_to_base64(image_input):
    """
    Punto de entrada universal para procesar imágenes y convertirlas a base64.
    Acepta múltiples formatos de entrada y devuelve una cadena base64 optimizada.

    Args:
        image_input: Puede ser:
            - Ruta de archivo (str)
            - Objeto de archivo con método read() (incluido _io.BufferedReader)
            - Bytes de imagen
            - Cadena base64

    Returns:
        str: Imagen en formato base64 optimizada para Spotify
    """
    try:
        print("\n=== PROCESANDO IMAGEN PARA SPOTIFY ===")

        # Caso 1: Si ya es una cadena base64
        if isinstance(image_input, str) and is_base64(image_input):
            print("Entrada detectada como cadena base64")
            img_data = base64.b64decode(image_input)
            print(
                f"Tamaño de imagen decodificada: {len(img_data) / 1024:.2f} KB")

        # Caso 2: Si es una ruta de archivo
        elif isinstance(image_input, str):
            print(f"Entrada detectada como ruta de archivo: {image_input}")
            if not os.path.exists(image_input):
                print(f"Error: No se encontró el archivo '{image_input}'")
                return None

            with open(image_input, 'rb') as f:
                img_data = f.read()
            print(f"Imagen leída desde archivo: {len(img_data) / 1024:.2f} KB")

        # Caso 3: Si es un objeto de archivo (_io.BufferedReader o similar)
        elif hasattr(image_input, 'read') and callable(getattr(image_input, 'read')):
            print(
                f"Entrada detectada como objeto de archivo: {type(image_input)}")

            # Verificar si podemos obtener la posición actual
            current_pos = 0
            try:
                if hasattr(image_input, 'tell'):
                    current_pos = image_input.tell()
            except:
                pass

            # Leer los datos del archivo
            try:
                img_data = image_input.read()
                print(
                    f"Imagen leída desde objeto: {len(img_data) / 1024:.2f} KB")
            except Exception as e:
                print(f"Error al leer del objeto de archivo: {e}")
                return None

            # Intentar regresar a la posición original
            try:
                if hasattr(image_input, 'seek'):
                    image_input.seek(current_pos)
            except:
                pass

        # Caso 4: Si son bytes directamente
        elif isinstance(image_input, bytes):
            print("Entrada detectada como bytes")
            img_data = image_input
            print(f"Tamaño de imagen: {len(img_data) / 1024:.2f} KB")

        else:
            print(f"Error: Tipo de entrada no soportado: {type(image_input)}")
            return None

        # Procesar la imagen para optimizar tamaño y formato
        processed_data = reduce_image_size(img_data)

        if not processed_data:
            print("Error al procesar la imagen.")
            return None

        # Convertir a base64
        base64_image = base64.b64encode(processed_data).decode('utf-8')
        print(
            f"Proceso completado. Longitud base64: {len(base64_image)} caracteres")

        return base64_image

    except Exception as e:
        print(f"Error en image_to_base64: {e}")
        import traceback
        traceback.print_exc()
        return None


def upload_playlist_cover(access_token, playlist_id, image_data):
    """
    Sube una imagen de portada a una playlist de Spotify.

    Args:
        access_token: Token de acceso de Spotify
        playlist_id: ID de la playlist
        image_data: Cadena base64 de la imagen o ruta de archivo o objeto de archivo

    Returns:
        int: Código de estado HTTP
    """
    import requests
    import json

    print("\n=== SUBIENDO IMAGEN A SPOTIFY ===")
    print(f"Playlist ID: {playlist_id}")

    # Convertir la imagen a base64 si no lo está ya
    if not isinstance(image_data, str) or not is_base64(image_data):
        print("Convirtiendo imagen a formato base64...")
        image_data = image_to_base64(image_data)

        if not image_data:
            print("Error al preparar la imagen para subir.")
            return None

    # URL para la API de Spotify
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"

    # Preparar encabezados
    if "Bearer " in access_token:
        auth_header = access_token
    else:
        auth_header = f'Bearer {access_token}'

    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }

    print(f"URL: {url}")
    print(
        f"Headers: Authorization: {auth_header[:20]}..., Content-Type: {headers['Content-Type']}")

    try:
        # Enviar solicitud a la API
        print("Enviando solicitud a Spotify...")
        response = requests.put(url, headers=headers,
                                data=json.dumps(image_data))

        # Manejar respuesta
        print(f"Respuesta: {response.status_code}")

        if response.status_code == 202:
            print("✅ Imagen subida exitosamente!")
        else:
            print(f"❌ Error {response.status_code} al subir imagen")
            try:
                print(f"Detalle: {response.json()}")
            except:
                print(f"Respuesta: {response.text}")

        return response.status_code

    except Exception as e:
        print(f"Error en la solicitud: {e}")
        import traceback
        traceback.print_exc()
        return None


# Ejemplo de uso
if __name__ == "__main__":
    # Probar con ruta de archivo
    ruta = input("Introduce la ruta de la imagen: ")
    img_base64 = image_to_base64(ruta)

    if img_base64:
        print("\nImagen procesada correctamente.")

        # Si quieres subir la imagen a Spotify
        upload = input("¿Quieres subir esta imagen a una playlist? (s/n): ")
        if upload.lower() == 's':
            token = input("Introduce tu token de Spotify: ")
            playlist = input("Introduce el ID de la playlist: ")
            upload_playlist_cover(token, playlist, img_base64)
