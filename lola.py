import requests
import base64
from dotenv import load_dotenv
import os

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Obtener el client_id y client_secret desde el archivo .env
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
    print(f"Access Token --> {access_token}")
else:
    print(f"Error: {response.status_code}")
    print(response.json())

# Encabezados de la solicitud
headers = {
    # Token de acceso obtenido previamente
    'Authorization': f'Bearer {access_token}'
}


# teniendo el accesToken podemos hacer peticiones a la API de Spotify

# # --- 1 obtener el id de un artista
# # https://api.spotify.com/v1/search?q=$ARTISTA&type=$ARTIST&limit=1

# # Parámetros de la solicitud
# artista = 'Coldplay'
# url = f'https://api.spotify.com/v1/search?q={artista}&type=artist&limit=1'


# # Realizar la solicitud GET
# response = requests.get(url, headers=headers)

# # Manejar la respuesta
# if response.status_code == 200:
#     data = response.json()
#     artistId = data['artists']['items'][0]['id']
#     # print(data['artists']['items'][0]['id'])
# else:
#     print(f"Error: {response.status_code}")
#     print(response.json())


# # --- 2 obtener Top Tracks
# # https://api.spotify.com/v1/artists/{artistId}/top-tracks

# # Parámetros de la solicitud
# url = f'https://api.spotify.com/v1/artists/{artistId}/top-tracks?market=US'

# # Realizar la solicitud GET
# response = requests.get(url, headers=headers)

# # Manejar la respuesta
# if response.status_code == 200:
#     data = response.json()
#     topTracks = data['tracks']
#     for track in topTracks:
#         print(f"{track['uri']} --- ")
# else:
#     print(f"Error: {response.status_code}")
#     print(response.json())

# --- 3 Obtener el userId
# curl --request GET \
#   --url https://api.spotify.com/v1/me \
#   --header 'Authorization: Bearer 1POdFZRZbvb...qqillRxMr2z'

# Parámetros de la solicitud
url = 'https://api.spotify.com/v1/me'

# Realizar la solicitud GET
response = requests.get(url, headers=headers)

# Manejar la respuesta
if response.status_code == 200:
    data = response.json()
    # userId = data['id']
    print('Me Data --> ', data)
else:
    print(f"Error: {response.status_code}")
    print(response.json())


# --- 4 Crear una lista
# creao una lista de reproducción
# https://api.spotify.com/v1/users/{client_id}/playlists

userId = '4gzpq5DPGxSnKTe4SA8HAU'
# Parámetros de la solicitud
url = f'https://api.spotify.com/v1/users/{userId}/playlists'
data = {
    'name': 'lolita',
    'description': 'prueba 01',
    'public': False
}

# # # Realizar la solicitud POST
# response = requests.post(url, headers=headers, data=data)

# # Manejar la respuesta
# if response.status_code == 201:
#     data = response.json()
#     print('playList --> ', data)
# else:
#     print(f"Error: {response.status_code}")
#     print(response.json())
