from spotifyApi.services.create_error_response import create_error_response


async def handle_error_response(response, artist_name, normalized_search_name):
    """Maneja respuestas de error de la API."""
    print(f"Error en la búsqueda del artista: {response.status}")
    error_text = await response.text()
    # Mostrar solo los primeros 200 caracteres
    print(f"Detalles del error: {error_text[:200]}...")

    # Si es un error 400 o 401, puede ser un problema con el token
    if response.status in (400, 401):
        print("Error de autenticación. Verifica el token de acceso.")
        return create_error_response("auth-error", normalized_search_name, artist_name)

    return None
