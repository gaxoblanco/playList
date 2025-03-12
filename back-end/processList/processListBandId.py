import asyncio
import os
import sys
import unicodedata
import asyncio
from typing import TypedDict, List, Dict, Any
import warnings
from spotifyApi.spotify_api import search_artist
from spotifyApi.dataBase_operations import search_band_db, add_band, search_bands_db_from_list
from services.merge_sort_bands import merge_and_sort_bands
from services.add_id_work_to_bands import add_id_work_to_bands
from processList.services.normalize_band_name import normalize_band_name
# Añadir el directorio padre al path para poder importar
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Conjunto global de bandas procesadas
processed_bands = set()


class BandData(TypedDict):
    id: int
    band_id: str
    name: str
    img: str
    date_create: str
    date_up: str
    genres: List[str]
    popularity: int
    message: str  # Para manejar posibles mensajes de error


# def normalize_band_name(band_name):
#     # Normalizar el nombre de la banda a minúsculas y eliminar caracteres especiales
#     band_name = band_name.strip().lower()
#     band_name = unicodedata.normalize('NFKD', band_name).encode(
#         'ASCII', 'ignore').decode('ASCII')
#     return band_name


async def process_list_band_id(access_token, bands_list):
    """
    Procesa una lista de bandas, verifica si existen en la base de datos,
    busca las que no existen en Spotify y las añade a la base de datos.
    Args:
        bands_list: Lista de diccionarios con información de bandas
                    [{'band_id': '', 'name': 'nombre', 'img_zone': [x, y, width, height]}]
    Returns:
        Lista actualizada con los IDs de las bandas y toda la información disponible
    """
    if not bands_list or not isinstance(bands_list, list):
        return {"error": "La entrada debe ser una lista de bandas"}, 400
    if not access_token:
        return {"error": "El token de acceso es obligatorio"}, 400
    # Le agrego un indice de trabajo y normalizo el nombre
    bands_list = add_id_work_to_bands(bands_list)
    print('inicio con copias bands_list ->',
          [band["name"] for band in bands_list])

    processed_bands = []
    # Diccionario para llevar un registro de bandas en procesamiento
    processing_bands = {}
    # Lock para acceder al diccionario de manera segura
    bands_lock = asyncio.Lock()

    # Crear un semáforo para limitar a N peticiones concurrentes
    N = 5
    semaphore = asyncio.Semaphore(N)

    async def search_band(band_name, band_item):
        # Normalizamos el nombre de la banda para usarlo como clave
        normalized_name = normalize_band_name(band_name)

        # Verificar si esta banda ya está siendo procesada
        async with bands_lock:
            if normalized_name in processing_bands:
                print(
                    f"La banda '{band_name}' ya está siendo procesada, esperando...")
                # Esperar a que termine el procesamiento previo
                await processing_bands[normalized_name]
                print(f"Procesamiento previo de '{band_name}' completado")

                # Verificar si la banda ya fue añadida a la base de datos por otra tarea
                existing_band = search_band_db(normalized_name)
                if isinstance(existing_band, tuple):
                    existing_band, status_code = existing_band
                    if status_code in [400, 404, 500]:
                        print(
                            f"Error al buscar la banda '{band_name}': {status_code}")
                        return None

                if isinstance(existing_band, dict) and 'id' in existing_band:
                    print(
                        f"La banda '{band_name}' ya fue añadida por otro proceso")
                    # Actualizar el item con datos de la base de datos
                    band_item['band_id'] = existing_band.get('band_id', '')
                    band_item['name'] = existing_band.get('name', '')
                    band_item['img_url'] = existing_band.get('img_url', '')
                    band_item['popularity'] = existing_band.get(
                        'popularity', 0)
                    band_item['genres'] = existing_band.get('genres', [])
                    return band_item

            # Marcar esta banda como en procesamiento con un Future
            task_future = asyncio.Future()
            processing_bands[normalized_name] = task_future

        try:
            # No encontramos la banda en la DB, buscamos en Spotify
            print("Buscando en Spotify...", band_name, band_item)

            # Buscar la banda en Spotify
            spotify_data = await search_artist(access_token, band_name)

            if spotify_data and 'id' in spotify_data:
                # Añadir la banda a la base de datos
                result, status_code = add_band(spotify_data)

                # Si se añadió correctamente o ya existía
                if status_code in [201, 409]:
                    # Actualizar el item con datos de Spotify
                    band_item['band_id'] = spotify_data['id']
                    band_item['name'] = spotify_data.get('name', '')
                    band_item['img_url'] = spotify_data.get('img', '')
                    band_item['popularity'] = spotify_data.get('popularity', 0)
                    band_item['genres'] = spotify_data.get('genres', [])

                    # Si la banda ya existía, obtenemos su ID de la base de datos
                    if status_code == 409 and 'id' in result:
                        warnings.warn(
                            f"Banda '{band_name} - {spotify_data.get('name')}' ya existe en la base de datos.")

                    print("Banda añadida:", band_item)
                    return band_item
                else:
                    # Si hubo un error al añadir, añadimos solo lo que tenemos
                    band_item['error'] = "No se pudo guardar en la base de datos"
                    return band_item
            else:
                # No se encontró en Spotify, añadimos solo lo que tenemos
                band_item['error'] = "No se encontró en Spotify"
                return band_item
        finally:
            # Marcar el procesamiento como completado
            async with bands_lock:
                if not processing_bands[normalized_name].done():
                    processing_bands[normalized_name].set_result(True)

    # Función para procesar una banda
    async def process_band(band_item):
        # Validar que band_item sea un diccionario
        if not isinstance(band_item, dict):
            print(f"Error: band_item no es un diccionario: {band_item}")
            return None
        # Obtener el nombre de la banda
        band_name = band_item['name']

        # Validar que el nombre de la banda sea un string válido
        if not isinstance(band_name, str) or band_name.strip() == '':
            print(f"Error: Nombre de banda inválido o vacío: {band_item}")
            return None
        try:
            async with semaphore:  # Esto asegura que solo N tareas se ejecuten a la vez
                return await search_band(band_name, band_item)
        except Exception as e:
            print(f"Error al procesar la banda '{band_name}': {e}")

    # Quitar las entradas sin name y crear un conjunto para deduplicar
    unique_bands = {}
    for band in bands_list:
        if band.get('name', ''):
            # Usamos el nombre normalizado como clave para deduplicar
            key = normalize_band_name(band['name'])
            if key not in unique_bands:
                unique_bands[key] = band

    # Convertir el diccionario deduplicado de vuelta a una lista
    bands_to_process = list(unique_bands.values())

    # Consultamos en la DB cuales tenemos - y obtengo array de objetos band_id, name, img_zone, genres, popularity, img_url
    bands_in_db, bands_to_search = search_bands_db_from_list(bands_to_process)
    print(
        f"Lista original: {len(bands_list)} bands_in_db + bands_to_search: {len(bands_in_db)} + {len(bands_to_search)}")  # type: ignore
    # imrpimo los name de bands_to_search
    print('estan aca bands_to_search ->', [band["name"]
          for band in bands_to_search])  # type: ignore

    # Verificar que bands_to_search es una lista
    if not isinstance(bands_to_search, list):
        return {"error": "No tengo bandas a buscar en spotify"}, 500

    # Crear tareas para procesar la lista de strings
    tasks = [process_band(band) for band in bands_to_search]

    # Ejecutar todas las tareas en paralelo
    results = await asyncio.gather(*tasks)
    # Filtrar resultados para eliminar los None
    processed_results = [result for result in results if result is not None]

    print('results del search ->', processed_results[0])
    # print('bands_in_db ->', bands_in_db)
    # print("bands_to_search ->", processed_results[0:5])
    print("processed_results ->", len(processed_results))
    # print("bands_in_db ->", bands_in_db[0:5])  # type: ignore
    print("bands_in_db ->", len(bands_in_db))

    # Junto las 2 listas y las ordeno segun el id_work incremental
    processed_bands, duplicates = merge_and_sort_bands(
        bands_in_db, processed_results)

    # Verificar si hay duplicados y alertar al programador
    if duplicates:
        print(
            f"¡Atención! Se encontraron {len(duplicates)} bandas duplicadas.")
        for dup in duplicates:
            print(
                f"ID: {dup['id_work']}, Nombre DB: {dup['name_in_db']}, Nombre Spotify: {dup['name_processed']}")

    return processed_bands
