from urllib.parse import parse_qs, urlencode, urlparse
import requests
import base64
import os
from dotenv import load_dotenv
import webbrowser
from flask import Flask, request
import threading

# Cargar variables de entorno
load_dotenv()

# Datos de la app en Spotify
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = "user-read-private user-read-email playlist-modify-public playlist-modify-private"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"


def get_authorization_code():
    """
    Redirige al usuario a la página de autorización de Spotify y solicita el código manualmente.
    """
    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }

    # Crear la URL de autorización
    auth_url = f"{AUTH_URL}?{urlencode(auth_params)}"

    # Abrir el navegador para que el usuario otorgue permisos
    print("Se abrirá una ventana del navegador. Por favor, autoriza la aplicación.")
    print(auth_url)
    webbrowser.open(auth_url)

    # Pedir al usuario que introduzca el código de autorización
    print("\nDespués de autorizar, serás redirigido a una página.")
    print("Copia la URL completa de esa página y pégala aquí:")

    while True:
        redirected_url = input(
            "URL completa, ...callback?code='token': ").strip()

        # Parsear la URL y extraer el código
        parsed_url = urlparse(redirected_url)
        query_params = parse_qs(parsed_url.query)

        if 'code' in query_params:
            authorization_code = query_params['code'][0]
            return authorization_code
        else:
            print(
                "No se pudo encontrar el código de autorización en la URL proporcionada.")
            print("Por favor, asegúrate de copiar la URL completa e intenta de nuevo.")


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
        print("Data==>", tokens)
        return access_token, refresh_token
    else:
        print(f"Error al obtener el token de acceso: {response.status_code}")
        print(f"Respuesta del servidor: {response.text}")
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


def get_access_token_deprecate():
    """
    Obtiene el token de acceso para la API de Spotify.
    """
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(
        f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {'grant_type': 'client_credentials'}

    response = requests.post(auth_url, headers=headers, data=data)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print(f"Error en la autenticación: {response.status_code}")
        print(response.json())
        return None
