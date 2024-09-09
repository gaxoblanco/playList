from flask import Flask, request, redirect, session
from spotify_auth import get_auth_url, exchange_code_for_token
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Necesario para usar sesiones


@app.route('/')
def index():
    auth_url = get_auth_url()
    return f'<a href="{auth_url}">Iniciar sesión con Spotify</a>'


@app.route('/callback')
def callback():
    error = request.args.get('error')
    code = request.args.get('code')

    if error:
        return f"Error: {error}"

    token_info = exchange_code_for_token(code)
    if token_info:
        # Guardar el token en la sesión
        session['access_token'] = token_info['access_token']
        return "Autenticación exitosa. Puedes cerrar esta ventana y volver a tu aplicación."
    else:
        return "Error al obtener el token de acceso."


@app.route('/get-token')
def get_token():
    return session.get('access_token', 'No token available')


if __name__ == '__main__':
    app.run(port=5000)
