import requests
import json


def get_user_id(access_token):
    """
    Obtiene el ID del usuario autenticado.
    """
    url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        user_id = data['id']
        return user_id
    else:
        print(f"Error al obtener el ID del usuario: {response.status_code}")
        print(response.json())
        return None


def search_artist(access_token, artist_name):
    """
    Busca un artista por su nombre y devuelve su ID.
    """
    url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        artist_id = data['artists']['items'][0]['id']
        img = data['artists']['items'][0]['images'][0]['url']
        genres = data['artists']['items'][0]['genres']
        return {'id': artist_id, 'img': img, 'genres': genres}
    else:
        print(f"Error en la búsqueda del artista: {response.status_code}")
        print(response.json())
        return None


def search_option(access_token, artist_name):
    """
    Busca un artista por su nombre y devuelve 5 opciones de artistas.
    """
    url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=5'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)
    list = []
    if response.status_code == 200:
        # itero por los 5 artista que me devuelve la api
        for artist in response.json()['artists']['items']:
            print(f"ID: {artist['id']} - Artista: {artist['name']}")
            list.append(
                {'id': artist, 'name': artist['name'], 'img': artist['images'][0]['url']})
        return list
    else:
        print(f"Error en la búsqueda del artista: {response.status_code}")
        print(response.json())
        return None


def get_top_tracks(access_token, artist_id):
    """
    Obtiene las canciones principales de un artista por su ID.
    """
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        top_tracks = data['tracks']
        return top_tracks
    else:
        print(f"Error al obtener las pistas: {response.status_code}")
        print(response.json())
        return None


def create_playlist(access_token, user_id, playlist_name, json_file):
    """
    Crea una lista de reproducción para el usuario especificado.
    """
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'name': playlist_name,
        'description': 'Lista de reproducción creada desde la API',
        'public': False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        playlist_data = response.json()

        # Extraer solo la información relevante
        relevant_data = {
            'href': playlist_data['external_urls']['spotify'],
            'id': playlist_data['id'],
            'images': playlist_data['images'],
            'name': playlist_data['name']
        }
        # Llamar a la función para guardar los datos en el archivo JSON
        append_to_json_file(relevant_data, json_file)

        return relevant_data
    else:
        print(
            f"Error al crear la lista de reproducción: {response.status_code}")
        print(response.json())
        return None


def append_to_json_file(new_data, filename):
    """
    Agrega un nuevo objeto al array en un archivo JSON existente.
    Si el archivo no existe, lo crea y agrega el nuevo objeto como el primer elemento del array.
    """
    # Asegurarse de que el filename tenga la extensión .json
    if not filename.lower().endswith('.json'):
        filename += '.json'

    try:
        # Cargar los datos actuales del archivo JSON si existe, usando UTF-8
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(data, list):
                data = [data]  # Convertir a lista si no lo es
    except FileNotFoundError:
        # Si el archivo no existe, inicializar con un array vacío
        data = []
    except json.JSONDecodeError:
        # Si el archivo existe pero está vacío o mal formateado, inicializar con un array vacío
        data = []
    except UnicodeDecodeError:
        # Si hay un error de decodificación, intentar con 'latin-1'
        try:
            with open(filename, 'r', encoding='latin-1') as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = [data]
        except:
            # Si aún falla, inicializar con un array vacío
            data = []

    # Agregar los nuevos datos al array existente
    data.append(new_data)

    # Escribir de nuevo los datos al archivo JSON usando UTF-8
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Datos de la lista de reproducción guardados en {filename}")
