from spotify_auth import get_access_token, get_authorization_code
from process_list_band_id import process_list_band_id
from process_list_band_top import process_list_band_top
from spotify_api import search_artist, get_top_tracks, create_playlist, get_user_id


def main():
    """
    Función principal que coordina la interacción con la API de Spotify según la entrada del usuario.
    """
    print("Autenticando...")

    # Obtener el código de autorización
    authorization_code = get_authorization_code()

    if not authorization_code:
        print("No se pudo obtener el código de autorización.")
        return

    # Obtener el token de acceso y de actualización
    access_token, refresh_token = get_access_token(authorization_code)

    if not access_token:
        print("No se pudo autenticar.")
        return

    print("Autenticado correctamente.", access_token)

    user_id = None

    while True:
        print("\n--- Menú ---")
        print("1. Buscar artista")
        print("2. Obtener Top Tracks de un artista")
        print("3. Obtener mi User ID")
        print("4. Crear una lista de reproducción")
        print("5. Procesar lista de bandas desde JSON")
        print("6. Procesar lista de bandas para obtener las Top Tracks")
        print("7. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            # Buscar artista
            artista = input("Introduce el nombre del artista: ")
            artist_id = search_artist(access_token, artista)
            if artist_id:
                print(f"ID del artista {artista}: {artist_id}")

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
            # Crear lista de reproducción
            if not user_id:
                # Si aún no se ha obtenido el User ID, lo obtenemos ahora
                user_id = get_user_id(access_token)

            if user_id:
                playlist_name = input(
                    "Introduce el nombre de la lista de reproducción: ")
                playlist = create_playlist(
                    access_token, user_id, playlist_name)
                if playlist:
                    print(
                        f"Lista de reproducción creada: {playlist['name']} - ID: {playlist['id']}")

        elif opcion == '5':
            # Procesar lista de bandas desde un archivo JSON
            process_list_band_id(access_token)

        elif opcion == '6':
            # Procesar lista de bandas para obtener las Top Tracks
            process_list_band_top(access_token)

        elif opcion == '7':
            # Salir
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")


if __name__ == "__main__":
    main()
