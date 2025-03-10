def merge_and_sort_bands(bands_in_db, processed_results, reference_bands):
    # Primero, combina ambas listas
    processed_bands = bands_in_db + processed_results

    # Ordena la lista combinada según el orden en reference_bands
    def get_band_index(band):
        # Asumiendo que cada banda tiene un atributo o clave 'name'
        band_name = band['name']
        for i, ref_band in enumerate(reference_bands):
            if ref_band['name'] == band_name:
                return i
        # Si no está en la referencia, lo colocamos al final
        return len(reference_bands)

    # Ordenamos usando la función auxiliar
    processed_bands.sort(key=get_band_index)

    return processed_bands
