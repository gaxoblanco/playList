import asyncio
import threading
from spotifyApi.dataBase_operations import add_band
from spotifyApi.spotify_api import search_option
from time import sleep
from flask import current_app

from flask import Flask
from spotifyApi.dataBase_operations import db
# Crear la aplicación Flask
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gaston:blanco@localhost:3307/festivalmusic'
# db.init_app(app)


def search_option_with_background_storage(access_token, artist_name, app):
    """
    Versión sincrónica que inicia un hilo separado para almacenamiento
    """
    # Crear un nuevo loop de eventos para esta solicitud
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Obtener resultados (convertimos función asíncrona a síncrona)
        artist_list = loop.run_until_complete(
            search_option(access_token, artist_name))

        if artist_list and len(artist_list) > 0:
            # Iniciar un hilo separado para el almacenamiento
            storage_thread = threading.Thread(
                target=store_artists_in_thread,
                args=(artist_list, app),
                daemon=False  # False = el hilo continuará incluso si el programa principal termina
            )
            storage_thread.start()
            print("Hilo de almacenamiento iniciado")
            print("search_option_with_background_storage artist_list ->", artist_list)
            return artist_list  # Devolver resultados al usuario
        else:
            # retorno un json de error
            return {"error": "No se encontraron artistas"}
    finally:
        # Cerrar el loop de eventos al finalizar
        loop.close()


def store_artists_in_thread(artist_list, app):
    """
    Función que se ejecuta en un hilo separado para almacenar artistas en la BD
    """
    print("Iniciando almacenamiento en hilo separado...")

    # Contador para estadísticas
    successful_count = 0
    failed_count = 0
    already_exists_count = 0

    # Crear un contexto de aplicación usando la app que se pasó como argumento
    with app.app_context():
        for artist in artist_list:
            if artist['band_id'] != '-' and 'band_id' in artist:
                try:
                    # Transformar datos al formato esperado por add_band
                    formatted_artist = {
                        "id": artist['band_id'],                  # Spotify ID
                        # Nombre del artista
                        "name": artist['name'],
                        # URL de imagen o valor por defecto
                        "img": artist.get('img_url') or "no_image",
                        # Lista de géneros
                        "genres": artist.get('genres', []),
                        # Popularidad (opcional)
                        "popularity": artist.get('popularity', 0)
                    }

                    # Pequeña pausa para no sobrecargar la BD
                    sleep(0.2)

                    # Llamar a add_band con los datos formateados
                    result, status_code = add_band(formatted_artist)

                    # Manejar diferentes respuestas
                    if status_code == 201:
                        print(
                            f"✅ Artista '{artist['name']}' añadido correctamente (ID: {artist['band_id']})")
                        successful_count += 1
                    elif status_code == 409:
                        print(
                            f"⚠️ Artista '{artist['name']}' ya existía en la base de datos")
                        already_exists_count += 1
                    else:
                        print(
                            f"❌ Error al procesar artista '{artist['name']}' (status: {status_code}): {result.get('error', 'Error desconocido')}")
                        failed_count += 1

                except Exception as e:
                    print(
                        f"❌ Excepción al procesar artista '{artist['name']}': {str(e)}")
                    failed_count += 1

        # Mostrar resumen
        print("\n--- Resumen de almacenamiento ---")
        print(f"✅ Artistas añadidos exitosamente: {successful_count}")
        print(f"⚠️ Artistas que ya existían: {already_exists_count}")
        print(f"❌ Errores al añadir artistas: {failed_count}")
        print(f"Total procesado: {len(artist_list)}")
        print("Almacenamiento en hilo separado completado")
