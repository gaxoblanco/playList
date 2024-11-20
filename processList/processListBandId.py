import asyncio
import json
import time
import unicodedata
from spotifyApi.spotify_api import search_artist

# Conjunto global de bandas procesadas
processed_bands = set()


def normalize_band_name(band_name):
    # Normalizar el nombre de la banda a minúsculas y eliminar caracteres especiales
    band_name = band_name.strip().lower()
    band_name = unicodedata.normalize('NFKD', band_name).encode(
        'ASCII', 'ignore').decode('ASCII')
    return band_name


async def process_list_band_id(access_token, band_list):
    """
    Procesa cada banda en la lista y busca su información en Spotify de manera asíncrona.

    Args:
        access_token (str): Token de autenticación de Spotify.
        band_list (list): Lista de bandas a procesar.

    Returns:
        list: Lista con la información actualizada de cada banda.
    """
    # Crear un semáforo para limitar el número de consultas concurrentes
    # Ajusta el número según las políticas del tercero
    semaphore = asyncio.Semaphore(5)

    # Crear una lista de tareas para cada búsqueda de banda
    tasks = [process_single_band(access_token, band, semaphore)
             for band in band_list]
    # Ejecutar todas las tareas de manera concurrente y obtener los resultados
    resultado = await asyncio.gather(*tasks)

    # Contar cuántos elementos no tienen band_id
    count_no_band_id = sum(
        1 for band in resultado if band.get("band_id") == "-")

    print(f"Number of elements without band_id: {count_no_band_id}")

    return resultado


async def process_single_band(access_token, band, semaphore):
    """
    Procesa una sola banda buscando su información en Spotify.

    Args:
        access_token (str): Token de autenticación de Spotify.
        band (dict): Diccionario con información de la banda.
        semaphore (asyncio.Semaphore): Semáforo para limitar el número de consultas concurrentes.

    Returns:
        dict: Información actualizada de la banda.
    """
    band_name = band.get("name")
    img_zone = band.get("img_zone")
    print(f"Procesando img_zone --=: {img_zone}")
    if not band_name:
        print("Nombre de banda no encontrado en el archivo JSON.")
        return band

    if band.get("band_id"):
        print(f"La banda {band_name} ya tiene un ID asignado.")
        return band

    normalized_band_name = normalize_band_name(band_name)

    async with semaphore:
        for attempt in range(5):  # Intentar hasta 5 veces
            try:
                # Buscar la banda en Spotify
                artist_data = await search_artist(access_token, normalized_band_name)

                if artist_data and 'id' in artist_data and artist_data['id'] not in processed_bands:
                    # Crear un nuevo diccionario para la banda actualizada
                    band_data = {
                        "name": artist_data['name'],
                        "band_id": artist_data['id'],
                        "img": artist_data['img'],
                        "genres": artist_data['genres'],
                        "img_zone": img_zone
                    }
                    print(f"Banda encontrada y procesada: {band_data['name']}")
                    # Añadir la banda al conjunto de bandas procesadas
                    processed_bands.add(artist_data['id'])
                    return band_data
                else:
                    band_data = {
                        "name": band_name,
                        "band_id": "-",
                        "img": '-',
                        "genres": [],
                        "img_zone": img_zone
                    }
                    print(f"Banda no encontrada en Spotify: {band_name}")
                    return band_data

            except Exception as e:
                if '429' in str(e):
                    print(f"Error 429: Rate limit exceeded. Retrying after delay...")
                    await asyncio.sleep(2 ** attempt)  # Exponencial backoff
                else:
                    print(
                        f"Error procesando la banda '{band_name}' en intento {attempt + 1}: {e}")
                    await asyncio.sleep(2 ** attempt)  # Exponencial backoff

        # Si todos los intentos fallan, devolver la banda con datos por defecto
        band_data = {
            "name": band_name,
            "band_id": "-",
            "img": None,
            "genres": [],
            "img_zone": img_zone
        }
        return band_data
