# Opción 1: Diccionario y comprensión de listas (más eficiente)
def find_bands_dict_array(bands_names, bands_query):
    """
    Divide una lista de nombres de bandas en bandas encontradas y no encontradas.

    Args:
        band_names: ['caballeros de la quema', 'el plan de la mariposa', 'bersuit']
        bands_query: [<Band 84>, <Band 86>, <Band 88>] => id: 84, Name: Jóvenes Pordioseros, Spotify ID: 6UYY..., Image URL: https:..., Popularity: None

    Returns:
        Tupla con (bandas_encontradas, bandas_no_encontradas)
    """
    # Inicializamos las listas para los resultados
    found_bands = []
    not_found_bands = []

    # Creamos un diccionario para hacer la búsqueda más eficiente
    bands_dict = {band.names.lower(): band for band in bands_query}
    # print('bands_dict names', bands_dict)

    print('bands_names ->', bands_names)
    print('bands_dict ->', bands_dict)
    # Iteramos por los nombres a buscar
    for name in bands_names:
        # Buscamos el nombre en el diccionario (convertido a minúsculas para comparación)
        if name.lower() in bands_dict:
            # Si se encuentra, añadimos el objeto Band a found_bands
            found_bands.append(bands_dict[name.lower()])
        else:
            # Si no se encuentra, añadimos el name: string y img_zone:bands_names.img_zone
            not_found_bands.append(
                {'name': name})

    return found_bands, not_found_bands
