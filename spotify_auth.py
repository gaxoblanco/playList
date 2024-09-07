import requests
import base64
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def get_access_token():
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
