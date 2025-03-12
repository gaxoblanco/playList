
import asyncio
import aiohttp
from spotifyApi.services.create_error_response import create_error_response


async def execute_with_backoff(func, url, headers, artist_name, normalized_search_name, max_retries, base_delay):
    """
    Ejecuta una función con estrategia de backoff exponencial.

    Args:
        func: Función a ejecutar
        url: URL de la petición
        headers: Headers HTTP
        artist_name: Nombre del artista original
        normalized_search_name: Nombre normalizado para comparaciones
        max_retries: Número máximo de reintentos
        base_delay: Retraso base para el backoff

    Returns:
        El resultado de la función o un objeto de error
    """
    import random

    # Circuit Breaker pattern
    for attempt in range(max_retries + 1):
        try:
            # Llamada a la función que hace el trabajo real
            result = await func(url, headers, artist_name, normalized_search_name)
            if result:
                return result

        except asyncio.TimeoutError:
            print(f"Timeout al conectar con Spotify para {artist_name}")

        except aiohttp.ClientConnectorError as e:
            print(f"Error de conexión con Spotify: {str(e)}")

        except Exception as e:
            print(
                f"Error inesperado al buscar artista {artist_name}: {str(e)}")

        # Estrategia de Backoff Exponencial con Jitter
        # Punto clave: Aquí se implementa el backoff exponencial
        if attempt < max_retries:
            # La fórmula 2^attempt crea el crecimiento exponencial
            # El random.uniform añade jitter para evitar sincronización de reintentos
            delay = base_delay * (2 ** attempt) + random.uniform(0.1, 0.5)
            print(
                f"Reintentando búsqueda de {artist_name} en {delay:.2f} segundos (intento {attempt+1}/{max_retries})")
            # Espera creciente entre intentos
            await asyncio.sleep(delay)
        else:
            print(f"Se agotaron los reintentos para {artist_name}")
            return create_error_response("max-retries", normalized_search_name, artist_name)

    return None  # Este return no debería alcanzarse nunca, pero lo mantenemos por seguridad
