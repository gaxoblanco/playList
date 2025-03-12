from processList.services.normalize_band_name import normalize_band_name


def add_id_work_to_bands(bands_list):
    """
    Añade un identificador único 'id_work' a cada banda basado en su posición original en el array.

    Args:
        bands_list: Lista de diccionarios con información de bandas

    Returns:
        List: Lista de bandas con el campo 'id_work' añadido
    """
    result = []

    for idx, band in enumerate(bands_list):
        # Crear una copia del diccionario para no modificar el original
        band_with_id = band.copy()
        # Añadir id_work basado en la posición en el array
        band_with_id['id_work'] = idx
        # Normalizar el nombre de la banda
        band_with_id['name'] = normalize_band_name(band['name'])
        result.append(band_with_id)

    return result
