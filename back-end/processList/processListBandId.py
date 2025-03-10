import asyncio
import os
import sys
import unicodedata
import asyncio
from typing import TypedDict, List, Dict, Any
from spotifyApi.spotify_api import search_artist
from spotifyApi.dataBase_operations import search_band_db, add_band, search_bands_db_from_list
from services.merge_sort_bands import merge_and_sort_bands
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


def normalize_band_name(band_name):
    # Normalizar el nombre de la banda a minúsculas y eliminar caracteres especiales
    band_name = band_name.strip().lower()
    band_name = unicodedata.normalize('NFKD', band_name).encode(
        'ASCII', 'ignore').decode('ASCII')
    return band_name


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

    processed_bands = []

    # Crear un semáforo para limitar a N peticiones concurrentes
    N = 5
    semaphore = asyncio.Semaphore(N)

    async def search_band(band_name, band_item):
        # No encontramos la banda en la DB, buscamos en Spotify
        print("Buscando en Spotify...", band_name, band_item)
        # ya viene normalizado
        # normalized_band_name = normalize_band_name(band_name)

        # Buscar la banda en Spotify
        spotify_data = await search_artist(access_token, band_name)
        # print("spotify_data ->", spotify_data)
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
                    band_item['db_id'] = result['id']
                else:
                    band_item['db_id'] = result.get('band_id')
                return band_item
            else:
                # Si hubo un error al añadir, añadimos solo lo que tenemos
                band_item['error'] = "No se pudo guardar en la base de datos"
                return band_item
        else:
            # No se encontró en Spotify, añadimos solo lo que tenemos
            band_item['error'] = "No se encontró en Spotify"
            return band_item

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

        async with semaphore:  # Esto asegura que solo N tareas se ejecuten a la vez
            return await search_band(band_name, band_item)

    # Creamos el array de tareas
    bands_to_process = []

    # Quitar las entradas sin name
    bands_to_process = [band for band in bands_list if band.get('name', '')]

    # Consultamos en la DB cuales tenemos - y obtengo array de objetos band_id, name, img_zone, genres, popularity, img_url
    bands_in_db, bands_to_search = search_bands_db_from_list(bands_to_process)
    # print('bands_to_search ->', bands_to_search)
    # print('bands_in_db ->', bands_in_db)

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
    print("processed_results ->", len(processed_results))
    print("bands_in_db ->", len(bands_in_db))

    # Primero, agregamos todas las bandas de bands_in_db
    processed_bands = merge_and_sort_bands(
        bands_in_db, processed_results, bands_list)
    print('processed_bands ->', len(processed_bands))

    return processed_bands
