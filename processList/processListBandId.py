import json
from spotifyApi.spotify_api import search_artist


def process_list_band_id(access_token, json_file):
    """
    Procesa una lista de bandas desde un archivo JSON, busca cada banda en Spotify y actualiza el campo `band_id`.

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
            if artist_data:
                band["band_id"] = artist_data['id']  # Asignar el ID encontrado
                # Asignar la imagen encontrada
                band["img"] = artist_data['img']
                # Asignar los géneros encontrados
                band["genres"] = artist_data['genres']
                print(f"ID del artista {band_name}: {artist_data['id']}")
            else:
                band["band_id"] = "-"  # Si no se encuentra, asignar '-'
                band["img"] = None  # Asignar None si no se encuentra la imagen
                # Asignar una lista vacía si no se encuentran géneros
                band["genres"] = []
                print(f"Artista no encontrado: {band_name}")

        except Exception as e:
            band["band_id"] = "-"  # En caso de error, asignar '-'
            print(f"Error al procesar el artista {band_name}: {e}")

    # actualizo el json
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(band_list, f, indent=4, ensure_ascii=False)

    print(f"Archivo guardado exitosamente en {json_file}")
