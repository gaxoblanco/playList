import json
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
        if not band.get('top_tracks'):
            fail_count += 1
            failed_bands.append(band['name'])
            continue
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

                print(
                    f"Pistas añadidas a la playlist {playlist} para {band['name']}")
        except Exception as e:
            print(
                f"Error al añadir las pistas de {band['name']} a la playlist: {e}")
            fail_count += 1
            failed_bands.append(band['name'])

    # print(f"Pistas añadidas a la playlist {playlist['name']}")
    return {"top_add": success_count, "top_failed": fail_count, "failed_bands": failed_bands}
