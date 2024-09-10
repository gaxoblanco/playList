import json
from spotify_api import get_top_tracks


def process_list_band_top(access_token, json_file):
    """
    Procesa una lista de bandas desde un archivo JSON, obtiene las top tracks de Spotify y actualiza el archivo con la lista de canciones.

    Args:
        access_token (str): El token de autenticación de Spotify.
    """

    # Leer el archivo JSON con la lista de bandas
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            band_list = json.load(f)
    except FileNotFoundError:
        print(
            f"El archivo {json_file} no se encontró. Asegúrate de que el archivo existe y la ruta es correcta.")
        return
    except json.JSONDecodeError:
        print(
            f"Error al decodificar el archivo {json_file}. Asegúrate de que el archivo está bien formado.")
        return
    except UnicodeDecodeError:
        print(
            f"Error de codificación al leer el archivo {json_file}. Asegúrate de que el archivo está en formato UTF-8.")
        return

    # Iterar sobre cada banda en el listado
    for band in band_list:
        band_name = band.get("name")
        artist_id = band.get("band_id")

        if not artist_id or artist_id == '-':
            print(
                f"No se ha encontrado un ID de artista válido para {band_name}. Saltando...")
            continue

        try:
            # Obtener las top tracks del artista
            top_tracks = get_top_tracks(access_token, artist_id)

            if top_tracks:
                # Crear una lista de diccionarios con el nombre de la canción y su URI
                band["top_tracks"] = [
                    {"name": track['name'], "uri": track['uri']} for track in top_tracks]
                print(f"Top Tracks añadidos para {band_name}:")
                for track in band["top_tracks"]:
                    print(f"{track['name']} - URI: {track['uri']}")
            else:
                # Si no se encuentran canciones, dejar el campo vacío
                band["top_tracks"] = []
                print(f"No se encontraron Top Tracks para {band_name}.")

        except Exception as e:
            # En caso de error, asignar una lista vacía
            band["top_tracks"] = []
            print(f"Error al procesar las top tracks de {band_name}: {e}")

    # actualizo el json
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(band_list, f, ensure_ascii=False, indent=4)

    print(f"Proceso de obtención de Top Tracks completado. "
          f"El archivo {json_file} ha sido actualizado con la información de las Top Tracks.")
