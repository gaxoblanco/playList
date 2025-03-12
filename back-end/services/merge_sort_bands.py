def merge_and_sort_bands(bands_in_db, processed_results):
    """
    Combina las bandas existentes en la base de datos con los nuevos resultados procesados,
    evitando duplicados basándose en el id_work.

    Args:
        bands_in_db: Lista de bandas ya existentes en la base de datos
        processed_results: Lista de nuevas bandas procesadas

    Returns:
        Tupla con (lista combinada y ordenada de bandas únicas, lista de duplicados)
    """
    # Usar un diccionario para combinar, usando id_work como clave
    combined_bands = {}
    duplicates = []

    # Primero agregamos las bandas de la base de datos
    for band in bands_in_db:
        if 'id_work' in band:
            combined_bands[band['id_work']] = band

    # Luego agregamos/actualizamos con los resultados procesados
    for band in processed_results:
        if 'id_work' in band:
            # Si ya existe este id_work, es un duplicado
            if band['id_work'] in combined_bands:
                duplicates.append(band)
            combined_bands[band['id_work']] = band

    # Convertimos de vuelta a lista
    merged_bands = list(combined_bands.values())

    # Ordenamos por id_work
    sorted_bands = sorted(merged_bands, key=lambda x: x.get('id_work', 0))

    return sorted_bands, duplicates
