import json
import time
from spotifyApi.spotify_api import search_artist


def process_list_band_id(access_token, band_list):
    """
    Procesa una lista de bandas desde un archivo JSON, busca cada banda en Spotify y actualiza el campo `band_id`.

    Args:
        access_token (str): El token de autenticación de Spotify.
    """

    # Iterar sobre cada banda en el listado
    for band in band_list:
        band_name = band.get("name")
        if not band_name:
            print("Nombre de banda no encontrado en el archivo JSON.")
            continue

        # Valido que aun no tenga un ID asignado
        if band.get("band_id"):
            print(f"La banda {band_name} ya tiene un ID asignado.")
            continue

        try:
            # Buscar el artista en Spotify
            artist_data = search_artist(access_token, band_name.strip())
            # Valido que el band_name no sea distinto de artist_data
            if artist_data:
                # Asignar el ID encontrado
                band["band_id"] = artist_data['id']
                # band_name = artist_data['name']
                band["name"] = artist_data['name']
                # Asignar la imagen encontrada
                band["img"] = artist_data['img']
                # Asignar los géneros encontrados
                band["genres"] = artist_data['genres']
                print(
                    f"artist_data--name: {artist_data}")
            else:
                band["band_id"] = "-"  # Si no se encuentra, asignar '-'
                band["img"] = None  # Asignar None si no se encuentra la imagen
                # Asignar una lista vacía si no se encuentran géneros
                band["genres"] = []
                print(f"Artista no encontrado: {band_name}")
            # Agregar un pequeño retraso entre solicitudes para evitar problemas de tasa de solicitudes
            time.sleep(1)

        except Exception as e:
            band["band_id"] = "-"  # En caso de error, asignar '-'
            band["img"] = None
            band["genres"] = []
            band["name"] = band_name
            print(f"Error al procesar el artista {band_name}: {e}")

    return band_list

    # print(f"Archivo guardado exitosamente en {json_file}")
