import json
import requests


# def process_list_band_add_to_playlist(access_token, json_file):
#     """
#     Procesa el archivo JSON para añadir pistas a una lista de reproducción en Spotify.
#     """

#     # Asegurarse de que el filename tenga la extensión .json
#     if not json_file.lower().endswith('.json'):
#         json_file += '.json'

#     try:
#         with open(json_file, 'r', encoding='utf-8') as file:
#             data = json.load(file)
#     except FileNotFoundError:
#         print("El archivo JSON no se encontró.")
#         return
#     except json.JSONDecodeError:
#         print("Error al leer el archivo JSON.")
#         return

#     # Extraer la información de las pistas y la lista de reproducción
#     tracks = []
#     playlist_id = None

#     for item in data:
#         if 'top_tracks' in item:
#             for track in item['top_tracks']:
#                 tracks.append(track['uri'])
#         elif 'id' in item:
#             playlist_id = item['id']

#     if not playlist_id:
#         print("No se encontró la ID de la lista de reproducción en el JSON.")
#         return

#     if not tracks:
#         print("No se encontraron pistas en el JSON.")
#         return

#     # Añadir pistas a la lista de reproducción
#     add_tracks_to_playlist(access_token, playlist_id, tracks)


# def add_tracks_to_playlist(access_token, playlist_id, track_uris):
#     """
#     Añade pistas a una lista de reproducción en Spotify.
#     """
#     url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     # Dividir las URIs en lotes de 100 o menos
#     for i in range(0, len(track_uris), 50):
#         chunk = track_uris[i:i + 50]
#         data = {
#             "uris": chunk
#         }

#         response = requests.post(url, headers=headers, json=data)

#         if response.status_code == 201:
#             print(
#                 f"Pistas añadidas exitosamente a la lista de reproducción {playlist_id}.")
#         else:
#             print(f"Error al añadir pistas: {response.status_code}")
#             print(response.json())

import requests


def process_list_band_add_to_playlist(access_token, band_list_top_ten, playlist):
    """
    Procesa la lista de bandas y añade las pistas a una lista de reproducción en Spotify.

    Args:
        access_token (str): El token de autenticación de Spotify.
        band_list_top_ten (list): Lista de bandas con sus top tracks.
        playlist (dict): Información de la playlist creada en Spotify.
    """

    playlist_id = playlist['band_id']
    # print(f"playlist_id--*: {playlist_id}")
    # print(f"band_list_top_ten--*: {band_list_top_ten}")

    headers = {
        'Authorization': f'{access_token}',
        'Content-Type': 'application/json'
    }
    # devuelvo el resultado de exito o fracaso al obtener el top ten de las bandas
    success_count = 0
    fail_count = 0
    failed_bands = []

    for band in band_list_top_ten:
        try:
            track_uris = [track['uri'] for track in band.get('top_tracks', [])]
            if track_uris:
                url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
                payload = {
                    'uris': track_uris
                }
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()
                success_count += 1

                # print(
                #     f"Pistas añadidas a la playlist {playlist} para {band['name']}")
        except Exception as e:
            print(
                f"Error al añadir las pistas de {band['name']} a la playlist: {e}")
            fail_count += 1
            failed_bands.append(band['name'])

    print(f"Pistas añadidas a la playlist {playlist['name']}")
    return {"top_add": success_count, "top_failed": fail_count, "failed_bands": failed_bands}
