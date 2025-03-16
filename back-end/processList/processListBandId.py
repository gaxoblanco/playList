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
from services.normalize_band_name import normalize_band_name
from processList.services.already_search import already_search
from processList.services.validate_stats_code import validate_status_code
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
        result = await already_search(bands_lock, band_name, processing_bands, band_item)
        if result:
            return result

        try:
            # No encontramos la banda en la DB, buscamos en Spotify
            print("Buscando en Spotify...", band_name, band_item)

            # Buscar la banda en Spotify con Backoff Exponencial
            spotify_data = await search_artist(access_token, band_name)
            # print('search_artist spotify_data ->', spotify_data)
            if spotify_data and 'id' in spotify_data:
                # Verificamos que el ID no sea un código de error
                if not any(error_type in str(spotify_data['id']) for error_type in ["-timeout-", "-connection-error-", "-error-", "-circuit-open-"]):
                    # Tenemos la información válida, añadimos la banda a la DB
                    result, status_code = add_band(spotify_data)
                    # Validamos y actuamos según lo ocurrido
                    return validate_status_code(status_code, result, band_item, spotify_data, band_name)
                else:
                    # Es un ID con formato de error, devolvemos los datos sin intentar guardar
                    # Actualizar el item con datos de error
                    band_item['band_id'] = spotify_data['id']
                    band_item['name'] = spotify_data.get('name', '')
                    band_item['img_url'] = spotify_data.get('img', '')
                    band_item['popularity'] = spotify_data.get('popularity', 0)
                    band_item['genres'] = spotify_data.get('genres', [])
                    return band_item
            else:
                # No se encontró en Spotify, añadimos solo lo que tenemos
                return band_item
        finally:
            # Marcar el procesamiento como completado
            async with bands_lock:
                if not processing_bands[normalized_name].done():
                    processing_bands[normalized_name].set_result(True)

    # Orquestador principal de consultas -> Semáforos
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
        # Capturar cualquier excepción para evitar que el proceso se detenga
        except Exception as e:
            print(f"Error al procesar la banda '{band_name}': {e}")
            # devuelvo el item con un band_id = '-error-'
            band_item['band_id'] = '-error-'
            return band_item

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
    # print(f"Lista original: {len(bands_list)} bands_in_db + bands_to_search: {len(bands_in_db)} + {len(bands_to_search)}")  # type: ignore
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

    print('processed_results ->', len(processed_results))
    print('bands_in_db ->', len(bands_in_db))
    # Junto las 2 listas y las ordeno segun el id_work incremental
    processed_bands = merge_and_sort_bands(
        bands_in_db, processed_results)

    return processed_bands
