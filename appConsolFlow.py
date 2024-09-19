# Token flow para autenticar en Spotify desde la consola usando main.py

from flask import Flask, request, redirect, session
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Cargar variables de entorno
load_dotenv()

# Datos de la app en Spotify
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
        return f"Error: {error}"

    if state != session.get('state'):
        return "Error: State mismatch. Possible CSRF attack."

    # Aquí deberías llamar a una función para intercambiar el código por tokens
    # Por ejemplo: tokens = exchange_code_for_tokens(code)

    # Por ahora, simplemente devolvemos el código
    return f"Authorization code: {code}"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
