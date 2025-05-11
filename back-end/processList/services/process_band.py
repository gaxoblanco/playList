import asyncio
import traceback
from typing import Dict, Any, Optional
from .search_band import search_band


async def process_band(band_item: Dict[str, Any],
                       access_token: str,
                       semaphore: asyncio.Semaphore,
                       bands_lock: asyncio.Lock,
                       processing_bands: Dict[str, asyncio.Future]) -> Optional[Dict[str, Any]]:
    """
    Procesa una banda individual, controlando la concurrencia mediante semáforos.

    Args:
        band_item: Diccionario con información de la banda
        access_token: Token de acceso para la API de Spotify
        semaphore: Semáforo para limitar peticiones concurrentes
        bands_lock: Lock para acceder de manera segura al diccionario processing_bands
        processing_bands: Diccionario para llevar registro de bandas en procesamiento

    Returns:
        Diccionario con la información actualizada de la banda o None si ocurre un error
    """
    # Validar que band_item sea un diccionario
    if not isinstance(band_item, dict):
        print(f"Error: band_item no es un diccionario: {band_item}")
        return None

    # Obtener el nombre de la banda
    band_name = band_item.get('name', '')

    # Validar que el nombre de la banda sea un string válido
    if not isinstance(band_name, str) or band_name.strip() == '':
        print(f"Error: Nombre de banda inválido o vacío: {band_item}")
        return None

    try:
        print(f"Procesando banda: {band_name} (Pre-semaphore)")
        async with semaphore:  # Esto asegura que solo N tareas se ejecuten a la vez
            print(f"Procesando banda: {band_name} (Post-semaphore)")
            result = await search_band(
                access_token,
                band_name,
                band_item,
                bands_lock,
                processing_bands
            )
            print(f"Resultado para {band_name}: {result}")
            return result

    # Capturar cualquier excepción para evitar que el proceso se detenga
    except Exception as e:
        print(f"Error al procesar la banda '{band_name}': {str(e)}")
        print(f"Traceback completo: {traceback.format_exc()}")
        # devuelvo el item con un band_id = '-error-'
        band_item['band_id'] = '-error-'
        return band_item
