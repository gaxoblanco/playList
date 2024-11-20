import json
from spotifyApi.spotify_api import get_top_tracks


def process_list_band_top(access_token, band_list):
    """
    Procesa una lista de bandas, obtiene las top tracks de Spotify y actualiza la lista con la lista de canciones.

    Args:
        access_token (str): El token de autenticación de Spotify.
        band_list (list): Lista de bandas a procesar.
    """
    for band in band_list:
        try:
            print(f"Obteniendo top tracks para id {band['band_id']}...")
            # Obtener las top tracks de Spotify para la banda
            top_tracks = get_top_tracks(access_token, band['band_id'])
            # Añadir las top tracks al diccionario de la banda
            band['top_tracks'] = top_tracks
        except Exception as e:
            print(f"Error al obtener las top tracks para {band['name']}: {e}")

    return band_list
