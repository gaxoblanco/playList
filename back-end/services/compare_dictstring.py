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
    # Crear un conjunto para rastrear bandas ya asignadas
    assigned_bands = set()

    # Creamos un diccionario para hacer la búsqueda más eficiente
    bands_dict = {}
    for band in bands_query:
        lower_name = band.names.lower()
        print(f"Band in DB: '{band.names}' → '{lower_name}'")
        bands_dict[lower_name] = band
    # print('bands_dict names', bands_dict)
    # convertimos a minúsculas para comparación
    bands_names_lower = [name.lower() for name in bands_names]

    # Iteramos por los nombres a buscar
    for i, (original_name, lower_name) in enumerate(zip(bands_names, bands_names_lower)):
        print(f"Buscando banda {i}: '{original_name}' → '{lower_name}'")

        # Buscamos el nombre en el diccionario
        if lower_name in bands_dict and lower_name not in assigned_bands:
            # Si se encuentra, añadimos el objeto Band a found_bands
            found_band = bands_dict[lower_name]
            print(f"✓ Encontrado: '{lower_name}' → '{found_band.names}'")
            found_bands.append(found_band)
            assigned_bands.add(lower_name)  # Marcar como asignada
        else:
            # Si no se encuentra o ya fue asignada, añadimos a not_found
            if lower_name in bands_dict:
                print(f"⚠️ Colisión: '{lower_name}' ya fue asignada")
            else:
                print(f"✗ No encontrado: '{lower_name}'")
            not_found_bands.append({'name': original_name})

    return found_bands, not_found_bands
