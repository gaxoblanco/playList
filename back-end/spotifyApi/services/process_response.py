import asyncio
from services.normalize_band_name import normalize_band_name
from spotifyApi.services.create_error_response import create_error_response


async def process_successful_response(response, artist_name, normalized_search_name):
    """Procesa una respuesta exitosa de Spotify."""
    data = await response.json()

    # Verificar que hay resultados
    if not data['artists']['items']:
        print(f"No se encontraron resultados para: {artist_name}")
        return create_error_response("no-results", normalized_search_name, artist_name)

    # Obtener datos del artista
    artist = data['artists']['items'][0]
    artist_id = artist['id']
    img = artist['images'][0]['url'] if artist['images'] else ""
    genres = artist['genres']
    name = artist['name']
    popularity = artist['popularity']

    # Normalizar y comparar nombres
    normalized_result_name = normalize_band_name(name)
    names_match = normalized_search_name == normalized_result_name

    # Si los nombres no coinciden, marcar como error de coincidencia
    if not names_match:
        print(
            f"Nombre devuelto '{name}' no coincide con búsqueda '{artist_name}'")
        return create_error_response("mismatch", normalized_search_name, artist_name)

    # Esperar un pequeño intervalo entre solicitudes - Rate Limiting preventivo
    await asyncio.sleep(0.2)

    return {
        'id': artist_id,
        'img': img,
        'genres': genres,
        'name': name,
        'popularity': popularity
    }
