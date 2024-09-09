import requests
import base64
import os
import urllib.parse
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URLs base
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'


def get_access_token():
    """
    Obtiene un token de acceso usando el Authorization Code Flow.
    """
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    # 1. Redirigir al usuario para autenticar
    auth_url = get_auth_url()
    print(f"Ve a esta URL para autenticarte: {auth_url}")

    # 2. Obtener el código de autorización manualmente
    code = input("Introduce el código de autorización de la URL: ")

    # 3. Intercambiar el código de autorización por un token
    tokens = exchange_code_for_token(code)

    if tokens:
        print("Autenticado correctamente. Access token obtenido.")
        return tokens.get('access_token')
    else:
        print("No se pudo obtener el token de acceso.")
        return None


def get_auth_url():
    """
    Construye la URL de autenticación de Spotify donde el usuario debe ir para iniciar sesión.
    """
    client_id = os.getenv('CLIENT_ID')
    redirect_uri = os.getenv('REDIRECT_URI')
    scope = "user-read-private playlist-modify-public playlist-modify-private"

    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': scope
    }

    url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return url


def exchange_code_for_token(code):
    """
    Intercambia el código de autorización por un token de acceso y de actualización.
    """
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    redirect_uri = os.getenv('REDIRECT_URI')

    # Autenticación base64
    auth_header = base64.b64encode(
        f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()  # Devuelve tokens de acceso y actualización
    else:
        print(f"Error al obtener el token: {response.status_code}")
        print(response.json())
        return None


def refresh_access_token(refresh_token):
    """
    Refresca el token de acceso cuando este haya expirado.
    """
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    auth_header = base64.b64encode(
        f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print(f"Error al refrescar el token: {response.status_code}")
        print(response.json())
        return None
