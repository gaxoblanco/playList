import asyncio
from asyncio.log import logger
import base64
from datetime import datetime
import json
# from playlist_cover import update_playlist_cover
from service_main.manage_login_token import manage_login_token
from processList.processListBandAddToPlaylist import process_list_band_add_to_playlist
from processList.processListBandId import process_list_band_id
from processList.processListBandTop import process_list_band_top
from spotifyApi.spotify_api import search_artist, get_top_tracks, create_playlist, get_user_id
from spotifyApi.services.sincro_search import search_option_with_background_storage
from spotifyApi.spotify_auth import get_access_token, get_authorization_code
from detect_possible_errors import detect_possible_errors
from img_process.img_process import img_process

from flask import Flask
# Importa la instancia de db desde el archivo de modelos
from spotifyApi.dataBase_operations import db

# Crear la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gaston:blanco@localhost:3306/festivalmusic'
db.init_app(app)


def main():
    """
    Función principal que coordina la interacción con la API de Spotify según la entrada del usuario.
    """
    print("Autenticando...")

    access_token = manage_login_token()
    print("Autenticado correctamente.", access_token)

    # Preguntar al usuario por el nombre del archivo JSON con que vamos a trabajar
    while True:
        json_file = input(
            "Introduce el nombre del archivo JSON a procesar (con extensión .json): ")
        # Comprobar que el archivo tenga la texto
        if not json_file:
            print(
                "No se paso un archivo. Se usa por defecto listarepro.json")
            json_file = "listarepro.json"
        # Comprobar que el archivo tenga la extensión .json
        if not json_file.endswith('.json'):
            # si no la tiene se la añadimos
            json_file += '.json'
        # valido que el archivo exista en el directorio
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                bands_list = json.load(file)
            break  # Salir del bucle si el archivo se carga correctamente
        except FileNotFoundError:
            # si no existe el archivo, le pido que lo vuevla a intentar
            print("El archivo no existe. Inténtalo de nuevo.")

    user_id = None
    while True:
        print("\n--- Menú ---")
        print("1. Buscar artista")
        print("1.2 Buscar artista con almacenamiento en segundo plano")
        print("2. Obtener Top Tracks de un artista")
        print("3. Obtener mi User ID")
        print("4. Corroborar posibles errores en los nombres de las bandas")
        print("5. Crear una lista de reproducción")
        print("6. Procesar lista de bandas desde JSON")
        print("7. Procesar lista de bandas para obtener las Top Tracks")
        print("8. Procesar lista de bandas para añadir a una lista de reproducción")
        print("9. Procesar imagen para obtener texto")
        print("00. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            # Buscar artista
            artista = input("Introduce el nombre del artista: ")
            artist_data = asyncio.run(search_artist(access_token, artista))
            if artist_data:
                print(f"ID del artista {artista}: {artist_data}")
            else:
                print("Error: Artista no encontrado.")
        if opcion == '1.2':
            # Buscar artista
            artista = input("Introduce el nombre del artista: ")
            artist_data = search_option_with_background_storage(
                access_token, artista)
            if artist_data:
                print(f"ID del artista {artista}: {artist_data}")
            else:
                print("Error: Artista no encontrado.")

        elif opcion == '2':
            # Obtener Top Tracks de un artista
            artist_id = input("Introduce el ID del artista: ")
            top_tracks = get_top_tracks(access_token, artist_id)
            if top_tracks:
                print("Top Tracks:")
                for track in top_tracks:
                    print(f"{track['name']} - URI: {track['uri']}")

        elif opcion == '3':
            # Obtener el User ID del usuario autenticado
            user_id = get_user_id(access_token)
            if user_id:
                print(f"Tu User ID es: {user_id}")

        elif opcion == '4':
            print("Corroborando posibles errores en los nombres de las bandas...")
            # Corroborar que no existan 2 bandas en la misma entrada
            detect_possible_errors(json_file)

        elif opcion == '5':
            # Crear lista de reproducción
            if not user_id:
                # Si aún no se ha obtenido el User ID, lo obtenemos ahora
                user_id = get_user_id(access_token)
                print(f"Tu User ID es: {user_id}")

            if user_id:
                playlist_name = input(
                    "Introduce el nombre de la lista de reproducción: ")
                playlist = create_playlist(
                    access_token, user_id, playlist_name)
                if playlist:
                    print(
                        f"Lista de reproducción creada: {playlist}")

        elif opcion == '6':
            # Procesar lista de bandas desde un archivo JSON
            try:
                with open(json_file, 'r', encoding='utf-8') as file:
                    bands_list = json.load(file)

                # Añade el contexto de la aplicación aquí
                with app.app_context():
                    result, report = asyncio.run(
                        process_list_band_id(access_token, bands_list))
                    print(
                        f"Resultado del procesamiento {len(result)} ->: {result}")
            except Exception as e:
                logger.error(f"Error al procesar la lista de bandas: {e}")

        elif opcion == '7':
            # Procesar lista de bandas para obtener las Top Tracks
            process_list_band_top(access_token, json_file)

        elif opcion == '8':
            print("Procesando lista de bandas para obtener las Top Tracks")
            # Procesar lista de bandas para añadir a una lista de reproducción
            bandListTopTen = process_list_band_top(access_token, json_file)
            print("Procesando lista de bandas para añadir a una lista de reproducción...")
            # Procesar lista de bandas para añadir a una lista de reproducción
            process_list_band_add_to_playlist(
                access_token, bandListTopTen, playlist)
        elif opcion == '9':
            # Le solicito al usuario la ruta de la imagen a procesar
            ruta_img = input(
                "Introduce la ruta de la imagen a procesar con el nombre: ")

            # si la rita esta vacia, se usa una por defecto
            if not ruta_img:
                ruta_img = 'imageQ.jpg'

            # Valido si termina con .jpg, si no se lo agrego
            if not ruta_img.endswith('.jpg'):
                ruta_img += '.jpg'

            # Primero convierto la imagen a base64
            with open(ruta_img, "rb") as img_file:
                # Leo el archivo binario
                binary_data = img_file.read()
                # Codifico a base64
                base64_encoded = base64.b64encode(binary_data)
                # Convierto de bytes a string y agrego el prefijo de datos
                img_base64 = f"data:image/jpeg;base64,{base64_encoded.decode('utf-8')}"
                img_result = img_process(img_base64)
            # Ahora puedo llamar a main con la imagen en base64
            print(f'resutlado de procesar la img ->', img_result)
            # Valido si el archivo prueva.json existe, si existe remplazo la informacion con img_result
            # Valido si el archivo prueva.json existe, si existe remplazo la informacion con img_result
            with open('prueva.json', 'w', encoding='utf-8') as file:
                json.dump(img_result, file)

        elif opcion == '00':
            # Salir
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")


if __name__ == "__main__":
    main()
