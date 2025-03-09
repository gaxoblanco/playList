import asyncio
import os
import sys
import unicodedata
from typing import TypedDict, List, Dict, Any
from spotifyApi.spotify_api import search_artist
from spotifyApi.dataBase_operations import search_band_db, add_band
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
    popularidad: int
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

    for band_item in bands_list:
        band_name = band_item.get('name', '')
        img_zone = band_item.get('img_zone', None)

        if not band_name:
            continue  # Saltamos las bandas sin nombre

        # Buscar la banda en la base de datos
        db_result = search_band_db(band_name)
        # Si encontramos la banda en la base de datos
        if isinstance(db_result, list) and len(db_result) > 0:
            print("db_result ->", db_result)
            # Tomar la primera coincidencia
            band_data: BandData = db_result[0]

            # Actualizar el item con los datos de la base de datos
            band_item['band_id'] = band_data['band_id']
            band_item['name'] = band_data['name']
            band_item['img'] = band_data['img']
            band_item['popularity'] = band_data.get('popularity', 0)
            band_item['genres'] = band_data['genres']

            # Mantenemos img_zone tal como está
            processed_bands.append(band_item)
        else:  # No encontramos la banda en la DB, buscamos en Spotify
            print("No se encontró en la base de datos, buscando en Spotify...")
            normalized_band_name = normalize_band_name(band_name)
            # Buscar la banda en Spotify
            spotify_data = await search_artist(access_token, normalized_band_name)
            print("spotify_data ->", spotify_data)
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

                    processed_bands.append(band_item)
                else:
                    # Si hubo un error al añadir, añadimos solo lo que tenemos
                    band_item['error'] = "No se pudo guardar en la base de datos"
                    processed_bands.append(band_item)
            else:
                # No se encontró en Spotify, añadimos solo lo que tenemos
                band_item['error'] = "No se encontró en Spotify"
                processed_bands.append(band_item)

    return processed_bands
