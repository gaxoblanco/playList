import asyncio
import random
from time import sleep
import time
import aiohttp
import requests
from services.normalize_band_name import normalize_band_name
from spotifyApi.services.circuit_breaker import CircuitBreaker
from spotifyApi.services.fetch_artist_data import fetch_artist_data
from spotifyApi.services.create_error_response import create_error_response

# Crear un Circuit Breaker global para el servicio de Spotify
spotify_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_time=60)
# Variables globales para el circuit breaker
consecutive_failures = 0
MAX_CONSECUTIVE_FAILURES = 5
circuit_open = False
last_failure_time = 0
CIRCUIT_RESET_TIME = 300  # 5 minutos en segundos


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
    global consecutive_failures, circuit_open, last_failure_time

# Comprobar si el circuit breaker está abierto (cortado)
    current_time = time.time()
    if circuit_open:
        # Verificar si ha pasado suficiente tiempo para resetear el circuit breaker
        if current_time - last_failure_time > CIRCUIT_RESET_TIME:
            print("Circuit breaker: Reseteando después del período de enfriamiento")
            circuit_open = False
            consecutive_failures = 0
        else:
            # Circuito abierto, devolver error sin intentar la búsqueda
            print(
                f"Circuit breaker: Abierto, omitiendo búsqueda de '{artist_name}'")
            return {
                'id': f"-circuit-open-{normalize_band_name(artist_name)}",
                'img': "img_error",
                'genres': [],
                'name': artist_name,
                'popularity': 0,
                'error_info': "Servicio temporalmente suspendido por múltiples fallos"
            }

    # Normalizamos el nombre original para comparar después
    normalized_search_name = normalize_band_name(artist_name)
    url = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Ejecutar con backoff exponencial
    result = await execute_with_circuit_breaker_and_backoff(
        fetch_artist_data,
        url,
        headers,
        artist_name,
        normalized_search_name,
        max_retries,
        base_delay
    )

    # Verificar si el resultado indica un error
    if result and any(error_type in str(result.get('id', '')) for error_type in
                      ["-timeout-", "-connection-error-", "-error-"]):
        # Incrementar contador de fallos consecutivos
        consecutive_failures += 1
        last_failure_time = current_time
        print(
            f"Circuit breaker: Incrementando contador de fallos a {consecutive_failures}")

        # Verificar si debemos abrir el circuit breaker
        if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
            circuit_open = True
            print(
                f"Circuit breaker: ABIERTO después de {consecutive_failures} fallos consecutivos")
    else:
        # Resetear contador de fallos si hay éxito
        if consecutive_failures > 0:
            print("Circuit breaker: Reseteando contador de fallos por respuesta exitosa")
            consecutive_failures = 0

    # Reportar el resultado para monitoreo si es un error
    if result and "-" in str(result.get('id', '')):
        print(
            f"Advertencia: La búsqueda de '{artist_name}' devolvió un resultado parcial: {result.get('id')}")

    return result


async def execute_with_circuit_breaker_and_backoff(func, *args, max_retries=3, base_delay=1.0, **kwargs):
    artist_name = args[2] if len(args) > 2 else "Unknown"
    normalized_search_name = args[3] if len(args) > 3 else "unknown"

    for attempt in range(max_retries + 1):
        try:
            # Intenta ejecutar la función
            result = await func(*args, **kwargs)
            # Si obtenemos un resultado, lo devolvemos inmediatamente
            if result:
                return result

        except asyncio.TimeoutError as e:
            print(f"Timeout al conectar con Spotify para {artist_name}")
            if attempt >= max_retries:
                # Crear respuesta de error formateada pero útil
                return {
                    'id': f"-timeout-{normalized_search_name}",
                    'img': "img_error",
                    'genres': [],
                    'name': artist_name,
                    'popularity': 0,
                    'error_info': "Timeout en la conexión con Spotify"
                }

        except aiohttp.ClientConnectorError as e:
            print(f"Error de conexión con Spotify: {str(e)}")
            if attempt >= max_retries:
                return {
                    'id': f"-connection-error-{normalized_search_name}",
                    'img': "img_error",
                    'genres': [],
                    'name': artist_name,
                    'popularity': 0,
                    'error_info': f"Error de conexión: {str(e)}"
                }

        except Exception as e:
            print(
                f"Error inesperado al buscar artista {artist_name}: {str(e)}")
            if attempt >= max_retries:
                return {
                    'id': f"-error-",
                    'img': "img_error",
                    'genres': [],
                    'name': artist_name,
                    'popularity': 0,
                    'error_info': f"Error: {str(e)}"
                }

        # Si no es el último intento, aplicar backoff
        if attempt < max_retries:
            # Backoff exponencial con jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0.1, 0.5)
            print(
                f"Reintentando búsqueda de {artist_name} en {delay:.2f} segundos (intento {attempt+1}/{max_retries})")
            await asyncio.sleep(delay)

    # Este punto solo se alcanza si hay un fallo en la lógica
    # Proporcionar un resultado por defecto para evitar que el proceso se rompa
    return {
        'id': f"-fallback-{normalized_search_name}",
        'img': "img_error",
        'genres': [],
        'name': artist_name,
        'popularity': 0,
        'error_info': "Falló por razón desconocida"
    }


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
