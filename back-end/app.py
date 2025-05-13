import asyncio
import copy
import json
from flask import (
    Flask,
    redirect,
    request,
    jsonify,
    session,
)
from flask_cors import CORS  # Importa CORS
import os
from dotenv import load_dotenv
from urllib.parse import urlencode
import secrets
from flask import Blueprint

from spotifyApi.spotify_auth import get_access_token
from spotifyApi.spotify_api import (
    create_playlist,
    get_user_id,
    upload_playlist_cover,
)
from spotifyApi.services.sincro_search import search_option_with_background_storage
from processList.processListBandId import process_list_band_id
from processList.processListBandAddToPlaylist import process_list_band_add_to_playlist
from processList.processListBandTop import process_list_band_top
from img_process.img_process import img_process
from img_process.img64 import image_to_base64
# from werkzeug.middleware.proxy_fix import ProxyFix

import logging
from logging.handlers import RotatingFileHandler
# Importa la instancia de db desde el archivo de modelos
from spotifyApi.dataBase_operations import db

# # Configuración de orígenes permitidos
# ALLOWED_ORIGINS = ["http://localhost:4200", "https://lineup.gaxoblanco.com"]

app = Flask(__name__, static_folder="static",
            static_url_path="", template_folder="static")
# Configurar CORS para toda la aplicación
CORS(app, resources={
     r"/API/*": {"origins": ["http://localhost:4200", "http://localhost:8000", "https://lineup.gaxoblanco.com"]}})

app.secret_key = secrets.token_hex(16)

# Truco para permitir enviar archivos grandes
MEGABYTE = (2 ** 10) ** 2
app.config['MAX_CONTENT_LENGTH'] = None
app.config['MAX_FORM_MEMORY_SIZE'] = 50 * MEGABYTE

# Configuración del logging
handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# Blueprint para las rutas de la API
api = Blueprint("api", __name__)


# Cargar variables de entorno
load_dotenv()
# Variables para la base de datos
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")  # os.getenv("REDIRECT_URI")
SCOPE = (
    "user-read-private user-read-email playlist-modify-public playlist-modify-private ugc-image-upload"
)

AUTH_URL = "https://accounts.spotify.com/authorize"

# Configuración de SQLAlchemy usando variables de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Inicializa la base de datos con la app
db.init_app(app)


@api.route("/login")
def login():
    """
    Inicia el proceso de autorización redirigiendo al usuario a la página de Spotify.
    """
    state = secrets.token_hex(16)
    session["state"] = state

    auth_params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "state": state,
    }

    auth_url = f"{AUTH_URL}?{urlencode(auth_params)}"
    return redirect(auth_url)


# Intercambio de tokens
@api.route("/callback", methods=["POST"])
def callback():
    """
    Maneja la redirección de Spotify después de la autorización.
    """
    error = request.args.get("error")
    state = request.args.get("state")
    data = request.get_json()

    code = data.get("code")

    if error:
        return jsonify({"error": error}), 400

# information_loading => Informacion random sobre bandas para el tiempo de espera
    # Aprobecho y le cargo un information_loading

    # intercambio de código por token de acceso
    tokens = get_access_token(code)  # --------
    # print("tokens:", tokens[1])
    return jsonify({"access_token": tokens[0], "refresh_token": tokens[1]})


@api.route("/up_img", methods=["POST"])
def up_img():
    """
    Sube una imagen a la API.
    """
    # Valido que la img esté en el body
    if "img" not in request.form:
        return jsonify({"error": "No image part"}), 400

    # Obtengo la img del body
    img64 = request.form["img"]

    # proceso la img con /img_process/img_process.main y espero la respuesta que va a demorar unos segundos
    img_json = img_process(img64)
    # print("img_json-->:", img_json)

    # img_json contiene el listado de bandas con erres
    # le envio el json al front
    return jsonify(img_json)


# ----------


@api.route("/band_list", methods=["POST"])
def band_list():
    """
    Procesa la lista de bandas y devuelve un JSON con la informacion de la banda
    """
    # if request.method == 'OPTIONS':
    #     return _build_cors_preflight_response()
    data = request.get_json()
    # obtengo access_token del header -> array de 1 string
    access_token = request.headers.get("Authorization")

    # print("access_token:", access_token)
    # print("json_file-band_list:", data)

    if not access_token:
        return jsonify({"error, token is required": data}), 400
    # Hacer una copia de data y pasarlo a la función para evitar modificar el objeto original
    bands_list = copy.deepcopy(data)
    print("data_copy:", bands_list)
    # Ejecuta el procesamiento asincrónico de las bandas
    with app.app_context():
        try:
            result = asyncio.run(
                process_list_band_id(access_token, bands_list))
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# ---------- search top 5 by name ----------
@api.route("/search_options", methods=["POST"])
def search_options():
    """
    Le envio al usuario las opciones de busqueda para la banda incorrecta que encontro
    """
    data = request.get_json()  # data === {'data': 'band name'}
    # obtengo access_token del header -> array de 1 string
    access_token = request.headers.get("Authorization")
    print("/search_options access_token:", access_token)
    if not access_token:
        return jsonify({"error, token is required": data}), 400

    # Extraer el nombre del artista del JSON recibido
    artist_name = data.get('data')
    if not artist_name:
        return jsonify({"error": "El nombre del artista es requerido -> {'data': 'band name'}"}), 400

    # Ejecutar la función asíncrona y obtener el resultado
    try:
        with app.app_context():
            option_list = search_option_with_background_storage(
                access_token, artist_name, app)
        return jsonify(option_list)
    except Exception as e:
        print(f"Error al buscar opciones del artista: {e}")
        return jsonify({"error": "Error en la búsqueda de opciones"}), 500


@api.route("/create_playlist", methods=["POST"])
def api_create_playlist():
    """
    Endpoint para crear una lista de reproducción.
    Requiere un token de acceso válido y los datos de la lista de reproducción.
    """
    # Captura el token de los headers
    access_token = request.headers.get("Authorization")
    # Obtener datos del formulario
    playlist_name = request.form.get("playlist_name")
    band_list = request.form.get("bandList")
    img = request.files.get("img")

    print("/create_playlist - img:")

    # Obtener el User ID del usuario autenticado
    user_id = get_user_id(access_token)
    if not access_token or not user_id or not playlist_name:
        return jsonify({"error": "Missing required data"}), 400

    # Crear la lista de reproducción
    playlist = create_playlist(access_token, user_id, playlist_name)
    print("playlist:", playlist)
    if not playlist:
        print(f"No se pudo crear la lista de reproducción: {playlist_name}")
        return jsonify({"error": "Failed to create playlist"}), 500

    # Obtengo el top ten de las bandas
    if band_list:
        band_listJSON = json.loads(band_list)
        print("band_listJSON:", band_listJSON)
        bandListTopTen = process_list_band_top(access_token, band_listJSON)
        print(
            "bandListTopTen -> :",
        )

    res = process_list_band_add_to_playlist(
        access_token, bandListTopTen, playlist)
    print("N° de bandas agregadas a la play list -> :", res)
    if res["top_failed"] == 0:
        return jsonify({"error": "Failed to add tracks to playlist"}), 500

    # Agregar portada del festival
    print("playlist data :", playlist)
    if img:
        print("img:", img)
        img64 = image_to_base64(img)
        if img64:
            img_status = upload_playlist_cover(
                access_token, playlist['playlist_id'], img64)
            print("img_status -> :", img_status)
        else:
            print("No se pudo procesar la imagen.")

    return jsonify(playlist, res)


# -------------------------------------------------------
# Registrar el blueprint en la app con el prefijo /API
app.register_blueprint(api, url_prefix="/API")

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
