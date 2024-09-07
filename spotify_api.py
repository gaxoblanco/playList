import requests


def get_user_id(access_token):
    """
    Obtiene el ID del usuario autenticado.
    """
    print('acces token obtenido --> ', access_token)
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
        error_data = response.json()
        error_message = error_data.get(
            'error', {}).get('message', 'Unknown error')
        raise Exception(f"Error {response.status_code}: {error_message}")


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
        return artist_id
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


def create_playlist(access_token, user_id, playlist_name):
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
        return playlist_data
    else:
        print(
            f"Error al crear la lista de reproducción: {response.status_code}")
        print(response.json())
        return None
