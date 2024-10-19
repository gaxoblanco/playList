import json
from flask import Flask, redirect, request, jsonify, session
from flask_cors import CORS  # Importa CORS
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import secrets
from spotifyApi.spotify_auth import get_access_token, get_authorization_code
from spotifyApi.spotify_api import create_playlist, search_option, get_top_tracks, get_user_id
from processList.processListBandId import process_list_band_id
from processList.processListBandAddToPlaylist import process_list_band_add_to_playlist
from detect_possible_errors import detect_possible_errors
import requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
# Habilita CORS en toda la aplicación
CORS(app, origins=["http://localhost:4200"],
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     allow_headers=["Content-Type", "Authorization", "code", "data"])


# Cargar variables de entorno
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = "user-read-private user-read-email playlist-modify-public playlist-modify-private"

AUTH_URL = "https://accounts.spotify.com/authorize"


@app.route('/login')
def login():
    """
    Inicia el proceso de autorización redirigiendo al usuario a la página de Spotify.
    """
    state = secrets.token_hex(16)
    session['state'] = state

    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state
    }

    auth_url = f"{AUTH_URL}?{urlencode(auth_params)}"
    return redirect(auth_url)


# Intercambio de tokens
@app.route('/callback', methods=['POST'])
def callback():
    """
    Maneja la redirección de Spotify después de la autorización.
    """
    error = request.args.get('error')
    state = request.args.get('state')
    data = request.get_json()

    code = data.get('code')

    if error:
        return jsonify({"error": error}), 400

    if state != session.get('state'):
        return jsonify({"error": "State mismatch. Possible CSRF attack."}), 403

    # print("body code:", code)

    # intercambio de código por token de acceso
    tokens = get_access_token(code)  # --------
    print("tokens:", tokens[1])
    return jsonify({"access_token": tokens[0], "refresh_token": tokens[1]})


@app.route('/up_img', methods=['POST'])
def up_img():
    """
    Sube una imagen a la API.
    """
    # obtengo la img de la body
    img = request.files['img']

    # proceso la img con /img_process/img_process.py
    # img_json = img_process(img)

    # img_json contiene el listado de bandas con erres
    # le envio el json al front
    # return jsonify(img_json)

    # return jsonify({"message": "Image uploaded successfully."})

# ----------

    def load_json_file(file_path):
        absolute_path = os.path.join(os.path.dirname(__file__), file_path)
        # Validate that the file exists
        if not os.path.exists(absolute_path):
            return absolute_path
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                band_list = json.load(f)
            return band_list
        except Exception as e:
            return {"error": str(e)}

    # le envio el archivo quilmesRock2025.json
    json_data = load_json_file('quilmesRock_3.json')
    # espera 10 segundos antes de responder
    # time.sleep(3)
    return jsonify(json_data)


@app.route('/band_list', methods=['POST', 'OPTIONS'])
def band_list():
    """
    Procesa la lista de bandas y devuelve un JSON con la informacion de la banda
    """
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    data = request.get_json()
    # obtengo access_token del header -> array de 1 string
    access_token = request.headers.get('Authorization')
    # Eliminar el prefijo 'Bearer ' si está presente
    if access_token and access_token.startswith('Bearer '):
        access_token = access_token.split(' ')[1]

    print("access_token:", access_token)
    print("json_file:", data)

    if not access_token:
        return jsonify({"error, token is required": data}), 400

    return jsonify(process_list_band_id(access_token, data))


# ---------- search top 5 by name ----------
@app.route('/search_options', methods=['POST', 'OPTIONS'])
def search_options():
    """
    Le envio al usuario las opciones de busqueda para la banda incorrecta que encontro
    """
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    data = request.get_json()
    # obtengo access_token del header -> array de 1 string
    access_token = request.headers.get('Authorization')
    # Eliminar el prefijo 'Bearer ' si está presente
    if access_token and access_token.startswith('Bearer '):
        access_token = access_token.split(' ')[1]

    print("access_token:", access_token)
    print("json_file:", data)

    if not access_token:
        return jsonify({"error, token is required": data}), 400

    option_list = search_option(access_token, data)
    return jsonify(option_list)


@app.route('/create_playlist', methods=['POST'])
def api_create_playlist():
    """
    Endpoint para crear una lista de reproducción.
    Requiere un token de acceso válido y los datos de la lista de reproducción.
    """
    data = request.get_json()
    access_token = data.get('Authorization')
    user_id = data.get('user_id')
    playlist_name = data.get('playlist_name')
    json_file = data.get('json_file')

    if not access_token or not user_id or not playlist_name:
        return jsonify({"error": "Missing required data"}), 400

    playlist = create_playlist(access_token, user_id, playlist_name, json_file)

    if playlist:
        return jsonify({"message": "Playlist created successfully", "playlist": playlist})
    else:
        return jsonify({"error": "Failed to create playlist"}), 500


@app.route('/process_list_band_add_to_playlist', methods=['POST'])
def process_list_band_add():
    """
    Endpoint para procesar lista de bandas y añadirlas a una playlist.
    """
    data = request.get_json()
    access_token = data.get('Authorization')
    json_file = data.get('json_file')

    process_list_band_add_to_playlist(access_token, json_file)

    return jsonify({"message": "List processed and added to playlist."})


def _build_cors_preflight_response():
    """ Construye la respuesta de preflight para OPTIONS """
    response = jsonify({"message": "CORS preflight passed"})
    response.headers.add("Access-Control-Allow-Origin",
                         "http://localhost:4200")
    response.headers.add("Access-Control-Allow-Headers",
                         "Content-Type,Authorization,access_token")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response


if __name__ == '__main__':
    app.run(port=5000, debug=True)
