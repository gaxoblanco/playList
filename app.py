import asyncio
import copy
import json
from flask import Flask, make_response, redirect, request, jsonify, session, render_template, send_from_directory
from flask_cors import CORS  # Importa CORS
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import secrets
from flask import Blueprint

import numpy as np
from spotifyApi.spotify_auth import get_access_token
from spotifyApi.spotify_api import create_playlist, search_option, get_user_id, upload_playlist_cover
from processList.processListBandId import process_list_band_id
from processList.processListBandAddToPlaylist import process_list_band_add_to_playlist
from processList.processListBandTop import process_list_band_top
from img_process.img_process import main
from img_process.img64 import image_to_base64
from werkzeug.middleware.proxy_fix import ProxyFix


# Configuración de orígenes permitidos
ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "https://festivalmusic.gaxoblanco.com"
]

app = Flask(__name__, static_folder='static',
            static_url_path='', template_folder='static')
app.secret_key = secrets.token_hex(16)

# Blueprint para las rutas de la API
api = Blueprint('api', __name__)

# Soporte para proxy más completo
app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_for=1,        # X-Forwarded-For
    x_proto=1,      # X-Forwarded-Proto
    x_host=1,       # X-Forwarded-Host
    x_port=1,       # X-Forwarded-Port
    x_prefix=1      # X-Forwarded-Prefix
)

# Configuración CORS más específica
CORS(app,
     resources={
         r"/API/*": {
             "origins": ALLOWED_ORIGINS,
             "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
             "allow_headers": ["Content-Type", "Authorization", "code", "data", "access_token"],
             "supports_credentials": True,  # Importante para las cookies/session
             "max_age": 3600
         }
     }
     )

# Antes de enturar a la ruta, hago un requerimiento de autorización


@app.after_request
def after_request(response):
    """Asegura que los headers CORS estén configurados consistentemente"""
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,code,data,access_token')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,OPTIONS,PUT,DELETE')
        response.headers.add('Access-Control-Max-Age', '3600')
    return response


# Cargar variables de entorno
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = "user-read-private user-read-email playlist-modify-public playlist-modify-private"

AUTH_URL = "https://accounts.spotify.com/authorize"


@api.route('/login')
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
@api.route('/callback', methods=['POST'])
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
    # print("tokens:", tokens[1])
    return jsonify({"access_token": tokens[0], "refresh_token": tokens[1]})


@api.route('/up_img', methods=['POST'])
def up_img():
    """
    Sube una imagen a la API.
    """
    # Valido que la img esté en el body
    if 'img' not in request.form:
        return jsonify({"error": "No image part"}), 400

    # Obtengo la img del body
    img64 = request.form['img']

    # proceso la img con /img_process/img_process.main y espero la respuesta que va a demorar unos segundos
    img_json = main(img64)
    # print("img_json-->:", img_json)
    # Antes de devolver el listado lo parseo

    # img_json contiene el listado de bandas con erres
    # le envio el json al front
    return jsonify(img_json)

# ----------


@api.route('/band_list', methods=['POST', 'OPTIONS'])
def band_list():
    """
    Procesa la lista de bandas y devuelve un JSON con la informacion de la banda
    """
    # if request.method == 'OPTIONS':
    #     return _build_cors_preflight_response()
    data = request.get_json()
    # obtengo access_token del header -> array de 1 string
    access_token = request.headers.get('Authorization')
    # Eliminar el prefijo 'Bearer ' si está presente
    if access_token and access_token.startswith('Bearer '):
        access_token = access_token.split(' ')[1]

    # print("access_token:", access_token)
    # print("json_file-band_list:", data)

    if not access_token:
        return jsonify({"error, token is required": data}), 400
    # Hacer una copia de data y pasarlo a la función para evitar modificar el objeto original
    data_copy = copy.deepcopy(data)
    # Ejecuta el procesamiento asincrónico de las bandas
    resultado = asyncio.run(process_list_band_id(access_token, data_copy))
    return jsonify(resultado)


# ---------- search top 5 by name ----------
@api.route('/search_options', methods=['POST', 'OPTIONS'])
def search_options():
    """
    Le envio al usuario las opciones de busqueda para la banda incorrecta que encontro
    """
    # if request.method == 'OPTIONS':
    #     return _build_cors_preflight_response()
    data = request.get_json()
    # obtengo access_token del header -> array de 1 string
    access_token = request.headers.get('Authorization')

    # print("access_token:", access_token)
    # print("json_file-search_options:", data)

    if not access_token:
        return jsonify({"error, token is required": data}), 400

    # Ejecutar la función asíncrona y obtener el resultado
    try:
        option_list = asyncio.run(search_option(access_token, data))
        return jsonify(option_list)
    except Exception as e:
        print(f"Error al buscar opciones del artista: {e}")
        return jsonify({"error": "Error en la búsqueda de opciones"}), 500


@api.route('/create_playlist', methods=['POST'])
def api_create_playlist():
    """
    Endpoint para crear una lista de reproducción.
    Requiere un token de acceso válido y los datos de la lista de reproducción.
    """
    # Captura el token de los headers
    access_token = request.headers.get('Authorization')
    # Obtener datos del formulario
    playlist_name = request.form.get('playlist_name')
    band_list = request.form.get('bandList')
    img = request.files.get('img')

    print("/create_playlist - img:", img)

    # Obtener el User ID del usuario autenticado
    user_id = get_user_id(access_token)
    if not access_token or not user_id or not playlist_name:
        return jsonify({"error": "Missing required data"}), 400

    # Crear la lista de reproducción
    playlist = create_playlist(access_token, user_id, playlist_name)
    if not playlist:
        print(f"No se pudo crear la lista de reproducción: {playlist_name}")
        return jsonify({"error": "Failed to create playlist"}), 500

    # Obtengo el top ten de las bandas
    if band_list:
        band_listJSON = json.loads(band_list)
        bandListTopTen = process_list_band_top(access_token, band_listJSON)
        print("bandListTopTen -> :",)

    res = process_list_band_add_to_playlist(
        access_token, bandListTopTen, playlist)
    print("N° de bandas agregadas a la play list -> :", res)
    if (res['top_failed'] == 0):
        return jsonify({"error": "Failed to add tracks to playlist"}), 500

    # Agregar portada del festival
    if img:
        img64 = image_to_base64(img)
        img_status = upload_playlist_cover(
            access_token, playlist['band_id'], img64)
        print("img_status -> :", img_status)

    return jsonify(playlist, res)


# -------------------------------------------------------
# Registrar el blueprint en la app con el prefijo /API
app.register_blueprint(api, url_prefix='/API')


# Ruta para servir otros archivos estáticos si es necesario (CSS, JS, imágenes, etc.)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static_files(path):
    # Verifica que app.static_folder no sea None
    if not app.static_folder:
        raise RuntimeError(
            "El directorio 'static_folder' no está configurado en la aplicación Flask.")

    # Si la ruta es para la API, devuelve un 404 porque no debe coincidir con archivos estáticos.
    if path.startswith('API'):
        return make_response("Not Found", 404)

    # -------------------------------------------------------
    # Lista de extensiones de archivos estáticos conocidos
    static_file_extensions = [
        '.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg',
        '.woff', '.woff2', '.ttf', '.eot', '.map', '.json'
    ]

    # Si la ruta termina con una extensión conocida, intenta servir el archivo estático
    if any(path.lower().endswith(ext) for ext in static_file_extensions):
        try:
            return send_from_directory(app.static_folder, path)
        except Exception as e:
            print(f"Error al servir archivo estático {path}: {str(e)}")
            return make_response("File not found", 404)

    # Para cualquier otra ruta, devuelve index.html para que Angular maneje el enrutamiento
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        print(f"Error al servir index.html: {str(e)}")
        return make_response("index.html not found", 404)


if __name__ == '__main__':
    # Configuraciones para producción
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
    app.run(port=5000, host='0.0.0.0')
