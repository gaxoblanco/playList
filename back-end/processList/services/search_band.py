import asyncio
from typing import Dict, Any
from services.normalize_band_name import normalize_band_name
from spotifyApi.spotify_api import search_artist
from spotifyApi.dataBase_operations import add_band
from processList.services.already_search import already_search
from processList.services.validate_stats_code import validate_status_code


async def search_band(access_token: str, band_name: str, band_item: Dict[str, Any],
                      bands_lock: asyncio.Lock, processing_bands: Dict[str, asyncio.Future]):
    """
    Busca una banda en Spotify y la añade a la base de datos si es necesario.

    Args:
        access_token: Token de acceso para la API de Spotify
        band_name: Nombre de la banda a buscar
        band_item: Diccionario con información de la banda
        bands_lock: Lock para acceder de manera segura al diccionario processing_bands
        processing_bands: Diccionario para llevar registro de bandas en procesamiento

    Returns:
        Diccionario con la información actualizada de la banda
    """
    # Normalizamos el nombre de la banda para usarlo como clave
    normalized_name = normalize_band_name(band_name)

    # Verificar si esta banda ya está siendo procesada
    result = await already_search(bands_lock, band_name, processing_bands, band_item)
    if result:
        return result

    try:
        # No encontramos la banda en la DB, buscamos en Spotify
        print(f"Buscando en Spotify: {band_name}")

        # Buscar la banda en Spotify con Backoff Exponencial
        spotify_data = await search_artist(access_token, band_name)

        if spotify_data and 'id' in spotify_data:
            # Verificamos que el ID no sea un código de error
            if not any(error_type in str(spotify_data['id']) for error_type in
                       ["-timeout-", "-connection-error-", "-error-", "-circuit-open-"]):
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
            if normalized_name in processing_bands and not processing_bands[normalized_name].done():
                processing_bands[normalized_name].set_result(True)
