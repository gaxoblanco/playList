
def find_band_positions(band_names, text_zones):
    """
    Encuentra las posiciones de las bandas asociando nombres con zonas de texto.
    Utiliza un enfoque mejorado para manejar nombres de varias palabras.
    """
    # Agrupamos palabras cercanas en la misma línea
    bands_with_positions = []
    processed_zones = set()  # Para marcar zonas ya procesadas

    for band in band_names:
        band_name = band['name'].upper()
        words = band_name.split()

        # Si el nombre tiene varias palabras, buscamos coincidencias secuenciales
        if len(words) > 1:
            best_match = find_multiword_band(
                words, text_zones, processed_zones)
            if best_match:
                bands_with_positions.append({
                    'name': band['name'],
                    'band_id': band['band_id'],
                    'img_zone': best_match
                })
                continue

        # Si no encontramos coincidencia con varias palabras o es una sola palabra
        # buscamos coincidencia directa
        found = False
        for i, zone in enumerate(text_zones):
            if i in processed_zones:
                continue

            zone_text = zone['text'].upper()
            # Comparamos primera palabra o texto completo
            if words[0] == zone_text or band_name == zone_text:
                bands_with_positions.append({
                    'name': band['name'],
                    'band_id': band['band_id'],
                    'img_zone': zone['position']
                })
                processed_zones.add(i)
                found = True
                break

        # Si no encontramos coincidencia
        if not found:
            bands_with_positions.append({
                'name': band['name'],
                'band_id': band['band_id'],
                'img_zone': None  # Sin posición encontrada
            })

    return bands_with_positions


def find_multiword_band(words, text_zones, processed_zones):
    """
    Busca una banda con múltiples palabras en las zonas de texto.
    Devuelve una posición compuesta que abarca todas las palabras.
    """
    for i, zone in enumerate(text_zones):
        if i in processed_zones:
            continue

        # Si encontramos la primera palabra
        if zone['text'].upper() == words[0]:
            # Verificamos si las siguientes palabras están en secuencia
            match_found = True
            matching_zones = [zone]
            word_index = 1

            # Buscamos en zonas siguientes las palabras restantes
            for j in range(i+1, len(text_zones)):
                if j in processed_zones:
                    continue

                if word_index >= len(words):
                    break

                next_zone = text_zones[j]
                # Verificamos que esté en la misma línea y sea la siguiente palabra
                same_line = next_zone['line_num'] == zone['line_num']
                same_block = next_zone['block_num'] == zone['block_num']
                is_next_word = next_zone['text'].upper() == words[word_index]

                # Si es la siguiente palabra y está en la misma línea
                if same_line and same_block and is_next_word:
                    matching_zones.append(next_zone)
                    word_index += 1
                    # Si ya no quedan palabras, encontramos coincidencia completa
                    if word_index >= len(words):
                        break

            # Si encontramos todas las palabras
            if word_index >= len(words):
                # Calculamos la posición completa (x, y, w, h)
                x = min(z['position'][0] for z in matching_zones)
                y = min(z['position'][1] for z in matching_zones)
                max_x = max(z['position'][0] + z['position'][2]
                            for z in matching_zones)
                max_y = max(z['position'][1] + z['position'][3]
                            for z in matching_zones)
                width = max_x - x
                height = max_y - y

                # Marcamos todas las zonas como procesadas
                for j, z in enumerate(text_zones):
                    if z in matching_zones:
                        processed_zones.add(j)

                return (x, y, width, height)

    return None  # No se encontró
