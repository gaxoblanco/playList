def merge_and_sort_bands(bands_in_db, processed_results):
    """
    Combina las bandas existentes en la base de datos con los nuevos resultados procesados,
    evitando duplicados basándose en el id_work.

    Args:
        bands_in_db: Lista de bandas ya existentes en la base de datos
        processed_results: Lista de nuevas bandas procesadas

    Returns:
        Tupla con (lista combinada y ordenada de bandas únicas, lista de duplicados, informe de coincidencias)
    """
    # Usar un diccionario para combinar, usando id_work como clave
    combined_bands = {}
    duplicates = []

    # Contadores para el informe
    mismatch_count = 0
    no_mismatch_count = 0

    # Primero agregamos las bandas de la base de datos
    for band in bands_in_db:
        if 'id_work' in band:
            combined_bands[band['id_work']] = band

            # Verificar si la banda tiene -error- en el band_id
            if 'band_id' in band and "-error-" in str(band['band_id']):
                mismatch_count += 1
            else:
                no_mismatch_count += 1

    # Luego agregamos/actualizamos con los resultados procesados
    for band in processed_results:
        if 'id_work' in band:
            # Si ya existe este id_work, es un duplicado
            if band['id_work'] in combined_bands:
                duplicates.append(band)
            else:
                # Verificar si la banda tiene mismatch con "queralt lahoz"
                if 'band_id' in band and "-error-" in str(band['band_id']):
                    mismatch_count += 1
                else:
                    no_mismatch_count += 1

            combined_bands[band['id_work']] = band

    # Convertimos de vuelta a lista
    merged_bands = list(combined_bands.values())

    # Ordenamos por id_work
    sorted_bands = sorted(merged_bands, key=lambda x: x.get('id_work', 0))

    # Crear informe
    report = {
        "total_bands": len(sorted_bands),
        "mismatch_queralt_lahoz": mismatch_count,
        "no_mismatch_queralt_lahoz": no_mismatch_count,
        "duplicates_found": len(duplicates)
    }

    print("--- INFORME DE BANDAS ---")
    print(f"Total de bandas: {report['total_bands']}")
    print(
        f"Bandas con mismatch 'queralt lahoz': {report['mismatch_queralt_lahoz']}")
    print(
        f"Bandas sin mismatch 'queralt lahoz': {report['no_mismatch_queralt_lahoz']}")
    print(f"Duplicados encontrados: {report['duplicates_found']}")
    print(f"Ejemplo formato de banda: {sorted_bands[0:4]}")
    print("------------------------")

    # return sorted_bands, duplicates, report
    return sorted_bands
