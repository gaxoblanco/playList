import asyncio
import json
import time
from spotifyApi.spotify_api import search_artist


# def process_list_band_id(access_token, band_list):
#     """
#     Procesa una lista de bandas desde un archivo JSON, busca cada banda en Spotify y actualiza el campo `band_id`.

#     Args:
#         access_token (str): El token de autenticación de Spotify.

#     Returns:
#         list: Lista con la información actualizada de cada banda.
#     """
#     # Inicializar una nueva lista para almacenar los resultados
#     resultado = []

#     # Iterar sobre cada banda en el listado
#     for band in band_list:
#         band_name = band.get("name")
#         if not band_name:
#             print("Nombre de banda no encontrado en el archivo JSON.")
#             continue

#         # Valido que aun no tenga un ID asignado
#         if band.get("band_id"):
#             print(f"La banda {band_name} ya tiene un ID asignado.")
#             resultado.append(band)
#             continue

#         try:
#             # Buscar el artista en Spotify
#             artist_data = search_artist(access_token, band_name.strip())
#             # Valido que el band_name no sea distinto de artist_data
#             if artist_data:
#                 # Crear un nuevo diccionario para la banda actual
#                 band_data = {
#                     "name": artist_data['name'],
#                     "band_id": artist_data['id'],
#                     "img": artist_data['img'],
#                     "genres": artist_data['genres']
#                 }
#                 print(
#                     f"artist_data--name: {artist_data}")
#             else:
#                 band_data = {
#                     "name": band_name,
#                     "band_id": "-",
#                     "img": None,
#                     "genres": []
#                 }
#                 print(f"Artista no encontrado: {band_name}")


#             resultado.append(band_data)
#             # Agregar un pequeño retraso entre solicitudes para evitar problemas de tasa de solicitudes
#             time.sleep(1)

#         except Exception as e:
#             band["band_id"] = "-"  # En caso de error, asignar '-'
#             band["img"] = None
#             band["genres"] = []
#             band["name"] = band_name
#             print(f"Error al procesar el artista {band_name}: {e}")

#     return resultado

# ----------------------------------
# Conjunto global de bandas procesadas
processed_bands = set()


def is_band_loaded(band_name, processed_bands):
    return band_name in processed_bands


async def process_list_band_id(access_token, band_list):
    """
    Procesa cada banda en la lista y busca su información en Spotify de manera asíncrona.

    Args:
        access_token (str): Token de autenticación de Spotify.
        band_list (list): Lista de bandas a procesar.

    Returns:
        list: Lista con la información actualizada de cada banda.
    """
    # Crear una lista de tareas para cada búsqueda de banda, solo si la banda no está cargada
    tasks = []
    # for band in band_list:
    #     if not is_band_loaded(band['name'], processed_bands):
    #         tasks.append(process_single_band(access_token, band))
    #         processed_bands.add(band['name'])
    # Crear una lista de tareas para cada búsqueda de banda
    tasks = [process_single_band(access_token, band) for band in band_list]
    # Ejecutar todas las tareas de manera concurrente y obtener los resultados
    resultado = await asyncio.gather(*tasks)

    # Contar cuántos elementos no tienen band_id
    count_no_band_id = sum(
        1 for band in resultado if band.get("band_id") == "-")

    print(f"Number of elements without band_id: {count_no_band_id}")

    return resultado


async def process_single_band(access_token, band):
    """
    Procesa una sola banda buscando su información en Spotify.

    Args:
        access_token (str): Token de autenticación de Spotify.
        band (dict): Diccionario con información de la banda.

    Returns:
        dict: Información actualizada de la banda.
    """
    band_name = band.get("name")
    if not band_name:
        print("Nombre de banda no encontrado en el archivo JSON.")
        return band

    if band.get("band_id"):
        print(f"La banda {band_name} ya tiene un ID asignado.")
        return band

    try:
        # Buscar la banda en Spotify
        # strip quita espacios adicionales
        artist_data = await search_artist(access_token, band_name.strip())

        if artist_data and 'id' in artist_data and artist_data['id'] not in processed_bands:
            # Crear un nuevo diccionario para la banda actualizada
            band_data = {
                "name": artist_data['name'],
                "band_id": artist_data['id'],
                "img": artist_data['img'],
                "genres": artist_data['genres']
            }
            print(f"Banda encontrada y procesada: {band_data['name']}")
            # Añadir la banda al conjunto de bandas procesadas
            processed_bands.add(artist_data['id'])
        else:
            band_data = {
                "name": band_name,
                "band_id": "-",
                "img": None,
                "genres": []
            }
            print(f"Banda no encontrada en Spotify: {band_name}")

    except Exception as e:
        print(f"Error procesando la banda '{band_name}': {e}")
        band_data = {
            "name": band_name,
            "band_id": "-",
            "img": None,
            "genres": []
        }

    return band_data
