import requests
import base64
import os
from dotenv import load_dotenv
import webbrowser
from urllib.parse import urlencode, urlparse, parse_qs

# Cargar variables de entorno
load_dotenv()

# Datos de la app en Spotify
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = "playlist-modify-public playlist-modify-private"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


def get_authorization_code():
    """
    Redirige al usuario a la página de autorización de Spotify.
    """
    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }

    # Crear la URL de autorización
    url = f"{AUTH_URL}?{urlencode(auth_params)}"

    # Abrir el navegador para que el usuario otorgue permisos
    webbrowser.open(url)

    # Pedir al usuario que introduzca la URL del callback después de autorizar
    redirected_url = input(
        "Introduce la URL a la que fuiste redirigido tras autorizar la app: ")

    # Extraer el código de autorización de la URL
    parsed_url = urlparse(redirected_url)
    authorization_code = parse_qs(parsed_url.query).get("code")

    if authorization_code:
        return authorization_code[0]
    else:
        print("No se pudo obtener el código de autorización.")
        return None


def get_access_token(auth_code):
    """
    Intercambia el código de autorización por un token de acceso y un token de actualización.
    """
    auth_header = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        return access_token, refresh_token
    else:
        print(f"Error al obtener el token de acceso: {response.status_code}")
        print(response.json())
        return None, None


def refresh_access_token(refresh_token):
    """
    Usa el token de actualización para obtener un nuevo token de acceso.
    """
    auth_header = base64.b64encode(
        f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

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
        access_token = response.json().get('access_token')
        return access_token
    else:
        print(f"Error al refrescar el token de acceso: {response.status_code}")
        print(response.json())
        return None
