
import asyncio
import aiohttp
from spotifyApi.services.process_response import process_successful_response
from spotifyApi.services.handle_error_response import handle_error_response


async def fetch_artist_data(url, headers, artist_name, normalized_search_name):
    """
    Realiza la petición a Spotify y procesa la respuesta.

    Args:
        url: URL de la API
        headers: Headers de autenticación
        artist_name: Nombre original del artista
        normalized_search_name: Nombre normalizado para comparaciones

    Returns:
        dict: Datos del artista o None si hay error
    """
    async with aiohttp.ClientSession() as session:
        # Timeout para evitar bloqueos prolongados
        timeout = aiohttp.ClientTimeout(total=10)
        async with session.get(url, headers=headers, timeout=timeout) as response:
            if response.status == 200:
                return await process_successful_response(response, artist_name, normalized_search_name)

            elif response.status == 429:  # Too Many Requests - Rate Limiting
                # Punto clave: Control específico para límite de tasa
                retry_after = int(response.headers.get('Retry-After', 1))
                print(
                    f"Límite de tasa excedido. Esperando {retry_after} segundos...")
                await asyncio.sleep(retry_after)
                return None  # Devolverá None para que el bucle principal reintente

            else:
                return await handle_error_response(response, artist_name, normalized_search_name)
