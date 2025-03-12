import asyncio
from time import sleep
import aiohttp
import requests
from processList.services.normalize_band_name import normalize_band_name


def get_user_id(access_token):
    """
    Obtiene el ID del usuario autenticado.
    """
    url = 'https://api.spotify.com/v1/me'
    headers = {
        'Authorization': f'{access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        user_id = data['id']
        return user_id
    else:
        print(f"Error al obtener el ID del usuario: {response}")
        print(response.json())
        return None


async def search_artist(access_token, artist_name, max_retries=3, base_delay=1.0):
    """
    Busca un artista por su nombre y devuelve su ID.
    Verifica que el nombre devuelto coincida con el buscado tras normalización.

    Args:
        access_token: Token de acceso para la API de Spotify
        artist_name: Nombre del artista a buscar
        max_retries: Número máximo de reintentos (por defecto: 3)
        base_delay: Tiempo de espera base en segundos (por defecto: 1.0)

    Returns:
        dict: Datos del artista o datos con formato de error si no coincide
    """
    import random

    # Normalizamos el nombre original para comparar después
    normalized_search_name = normalize_band_name(artist_name)

    url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    for attempt in range(max_retries + 1):
        try:
            async with aiohttp.ClientSession() as session:
                # Timeout para evitar bloqueos prolongados
                timeout = aiohttp.ClientTimeout(total=10)
                async with session.get(url, headers=headers, timeout=timeout) as response:
                    if response.status == 200:
                        data = await response.json()

                        # Verificar que hay resultados
                        if not data['artists']['items']:
                            print(
                                f"No se encontraron resultados para: {artist_name}")
                            return {
                                'id': f"-no-results-{normalized_search_name}",
                                'img': "img_error",
                                'genres': [],
                                'name': artist_name,
                                'popularity': 0
                            }

                        # Obtener datos del artista
                        artist = data['artists']['items'][0]
                        artist_id = artist['id']
                        img = artist['images'][0]['url'] if artist['images'] else ""
                        genres = artist['genres']
                        name = artist['name']
                        popularity = artist['popularity']

                        # Normalizar y comparar nombres
                        normalized_result_name = normalize_band_name(name)
                        names_match = normalized_search_name == normalized_result_name

                        # Si los nombres no coinciden, marcar como error de coincidencia
                        if not names_match:
                            print(
                                f"Nombre devuelto '{name}' no coincide con búsqueda '{artist_name}'")
                            return {
                                'id': f"-mismatch-{normalized_search_name}",
                                'img': "img_error",
                                'genres': [],
                                'name': artist_name,  # Mantenemos el nombre original
                                'popularity': 0
                            }

                        # Esperar un pequeño intervalo entre solicitudes
                        await asyncio.sleep(0.2)

                        return {
                            'id': artist_id,
                            'img': img,
                            'genres': genres,
                            'name': name,
                            'popularity': popularity
                        }

                    elif response.status == 429:  # Too Many Requests
                        # Leer el header Retry-After si está disponible
                        retry_after = int(
                            response.headers.get('Retry-After', 1))
                        print(
                            f"Límite de tasa excedido. Esperando {retry_after} segundos...")
                        await asyncio.sleep(retry_after)
                        continue  # Reintentar inmediatamente después de esperar

                    else:
                        print(
                            f"Error en la búsqueda del artista: {response.status}")
                        error_text = await response.text()
                        # Mostrar solo los primeros 200 caracteres
                        print(f"Detalles del error: {error_text[:200]}...")

                        # Si es un error 400 o 401, puede ser un problema con el token
                        if response.status in (400, 401):
                            print(
                                "Error de autenticación. Verifica el token de acceso.")
                            return {
                                'id': f"-auth-error",
                                'img': "img_error",
                                'genres': [],
                                'name': artist_name,
                                'popularity': 0
                            }

        except asyncio.TimeoutError:
            print(f"Timeout al conectar con Spotify para {artist_name}")

        except aiohttp.ClientConnectorError as e:
            print(f"Error de conexión con Spotify: {str(e)}")

        except Exception as e:
            print(
                f"Error inesperado al buscar artista {artist_name}: {str(e)}")

        # Si no es el último intento, esperar y reintentar
        if attempt < max_retries:
            # Backoff exponencial con jitter (variación aleatoria)
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            print(
                f"Reintentando búsqueda de {artist_name} en {delay:.2f} segundos (intento {attempt+1}/{max_retries})")
            await asyncio.sleep(delay)
        else:
            print(f"Se agotaron los reintentos para {artist_name}")
            return {
                'id': f"-max-retries-{normalized_search_name}",
                'img': "img_error",
                'genres': [],
                'name': artist_name,
                'popularity': 0
            }

    return None  # Este return no debería alcanzarse nunca, pero lo mantenemos por seguridad


async def search_option(access_token, artist_name):
    print("search_option access_token ->", access_token)
    """
    Busca un artista por su nombre y devuelve 5 opciones de artistas.
    """
    url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=10'
    headers = {
        'Authorization': f'{access_token}'
    }

    response = requests.get(url, headers=headers)
    artist_list = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                response_json = await response.json()  # Await the asynchronous call

                # Validar que la respuesta contenga la clave 'artists' y 'items'
                if 'artists' in response_json and 'items' in response_json['artists']:
                    items = response_json['artists']['items']

                    # Validar que 'items' sea una lista
                    if isinstance(items, list):
                        if items:
                            # Iterar por los artistas devueltos por la API
                            for artist in items:
                                artist_list.append({
                                    'band_id': artist.get('id', '-'),
                                    'name': artist.get('name', 'Unknown'),
                                    'img': artist['images'][0]['url'] if artist.get('images') else None,
                                    'href': artist['external_urls']['spotify'] if artist.get('external_urls') else None,
                                    'genres': artist.get('genres', [])
                                })
                        else:
                            # Si no se encontraron artistas, devolver un mensaje de error
                            artist_list.append({
                                'band_id': '-',
                                'name': 'Artista no encontrado',
                                'img': None,
                                'href': None,
                                'genres': []
                            })
                    else:
                        print("Error: 'items' no es una lista.")
                        return None
                else:
                    print("Error: Respuesta de la API no contiene 'artists' o 'items'.")
                    return None
            else:
                print(
                    f"Error en la búsqueda del artista: {response.status}")
                print(response.json())
                return None

    return artist_list


def get_top_tracks(access_token, artist_id):
    """
    Obtiene las canciones principales de un artista por su ID.
    """
    if artist_id == '-':
        # excape this elemente
        return None
    # print("artist_id ->", artist_id)
    # print("access_token ->", access_token)
    url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks'
    headers = {
        'Authorization': f'{access_token}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        top_tracks = data['tracks']
        return top_tracks
    else:
        print(f"Error al obtener las pistas: {response.status_code}")
        # print(response.json())
        return None


def create_playlist(access_token, user_id, playlist_name):
    """
    Crea una lista de reproducción para el usuario especificado.
    """
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = {
        'Authorization': f'{access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'name': playlist_name,
        'description': 'Play List creada desde www.gaxoblanco.com',
        'public': False
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        playlist_data = response.json()

        # Extraer solo la información relevante
        relevant_data = {
            'href': playlist_data['external_urls']['spotify'],
            'band_id': playlist_data['id'],
            'img': playlist_data['images'],
            'name': playlist_data['name']
        }

        return relevant_data
    else:
        print(
            f"Error al crear la lista de reproducción: {response.status_code}")
        # print(response.json())
        return None


def upload_playlist_cover(access_token, playlist_id, image_data):
    print("upload_playlist_cover access_token ->", access_token)
    print("upload_playlist_cover playlist_id ->", playlist_id)
    print("upload_playlist_cover image_data ->", image_data)

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"
    headers = {
        'Authorization': f'{access_token}',
        "Content-Type": "image/jpeg"  # Spotify requiere que sea un JPEG
    }

    response = requests.put(url, headers=headers, data=image_data)

    # Manejo de la respuesta
    if response.status_code == 202:
        print("Imagen de portada cargada exitosamente!")
    else:
        print(f"Error al cargar la imagen: {response.status_code}")
        try:
            print(response.json())  # Detalles del error si están disponibles
        except Exception as e:
            print(f"Error al decodificar la respuesta: {e}")
        return response.status_code
