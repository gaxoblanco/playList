from flask import Flask, redirect, request, jsonify, session
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import secrets
from spotifyApi.spotify_auth import get_access_token, get_authorization_code
from spotifyApi.spotify_api import create_playlist, search_artist, get_top_tracks, get_user_id
from processList.processListBandAddToPlaylist import process_list_band_add_to_playlist
from detect_possible_errors import detect_possible_errors
import requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

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


@app.route('/callback')
def callback():
    """
    Maneja la redirección de Spotify después de la autorización.
    """
    error = request.args.get('error')
    code = request.args.get('code')
    state = request.args.get('state')

    if error:
        return jsonify({"error": error}), 400

    if state != session.get('state'):
        return jsonify({"error": "State mismatch. Possible CSRF attack."}), 403

    # Aquí deberías llamar a una función para intercambiar el código por tokens
    tokens = get_access_token(code)

    return jsonify({"access_token": tokens[0], "refresh_token": tokens[1]})


@app.route('/create_playlist', methods=['POST'])
def api_create_playlist():
    """
    Endpoint para crear una lista de reproducción.
    Requiere un token de acceso válido y los datos de la lista de reproducción.
    """
    data = request.get_json()
    access_token = data.get('access_token')
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
    access_token = data.get('access_token')
    json_file = data.get('json_file')

    process_list_band_add_to_playlist(access_token, json_file)

    return jsonify({"message": "List processed and added to playlist."})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
