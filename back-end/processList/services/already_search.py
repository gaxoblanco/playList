import asyncio
from services.normalize_band_name import normalize_band_name
from spotifyApi.dataBase_operations import search_band_db


async def already_search(bands_lock, band_name, processing_bands, band_item):
    # Normalizamos el nombre de la banda para usarlo como clave
    normalized_name = normalize_band_name(band_name)
    async with bands_lock:
        if normalized_name in processing_bands:
            print(
                f"La banda '{band_name}' ya está siendo procesada, esperando...")
            # Esperar a que termine el procesamiento previo
            await processing_bands[normalized_name]
            print(f"Procesamiento previo de '{band_name}' completado")

            # Verificar si la banda ya fue añadida a la base de datos por otra tarea
            existing_band = search_band_db(normalized_name)
            if isinstance(existing_band, tuple):
                existing_band, status_code = existing_band
                if status_code in [400, 404, 500]:
                    print(
                        f"Error al buscar la banda '{band_name}': {status_code}")
                    return None

            if isinstance(existing_band, dict) and 'id' in existing_band:
                return existing_band

    return {}
