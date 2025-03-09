import re


def clean_and_split_text(text):
    # paso todo a minusculas
    text = text.lower()
    # Reemplazamos los separadores claros por saltos de línea
    text = re.sub(r'[+»«~*-.©¢_><;—]', '\n', text)

    # Dividimos el texto en líneas y eliminamos líneas vacías
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip()]

    # Creamos el array de objetos
    result = []
    for line in lines:
        # Separamos por salto de línea y eliminamos espacios extra
        names = [name.strip() for name in line.split('\n') if name.strip()]
        for name in names:
            # Inicializamos band_id vacío
            result.append({"name": name, "band_id": ""})

    return result


def limpiar_array(array):
    """
    Elimina los elementos que no contienen texto y solo contienen caracteres especiales, puntos o guiones.
    """
    # Expresión regular para capturar elementos que consisten únicamente en caracteres especiales, puntos o guiones
    caracteres_especiales = r'^[^\w\s]+$'
    array_limpio = []

    # Itero el array buscando elementos que NO contengan solo caracteres especiales, puntos o guiones
    for elemento in array:
        if re.search(caracteres_especiales, elemento['text']) is None:
            array_limpio.append(elemento)

    return array_limpio

# itero apartir de la posicion encontrada para buscar el resto de la palabra y obtener el with de la suma de las palabras


def obtener_posicion_final(full_name, text_zone, indexStart):
    palabras = full_name.split()
    for i in range(indexStart+1, len(text_zone)):
        # si la palabra no coincide con la siguiente palabra de la banda, salgo del loop
        if i - indexStart - 1 >= len(palabras) or text_zone[i]['text'].upper() != palabras[i - indexStart - 1].upper():
            break
        # si coincide la ultima palabra de la banda con la ultima palabra de la zona, guardo la posicion
        if i == indexStart + len(palabras) - 1:
            return i
    return indexStart  # Devuelve indexStart si no encuentra la posición final

# itero y sumo todos los valores de W H dentro de img_zone[X, Y, W, H]


def obtener_with_height(indexStart, indexFinish, text_zone):
    # itero del indexStart al indexFinish sobre text_zone.position y sumo los valores de W y H que son [X, Y, W, H] == [0, 1, 2, 3]
    with_height = [0, 0]
    for i in range(indexStart, indexFinish+1):
        with_height[0] += text_zone[i]['position'][2]
        with_height[1] += text_zone[i]['position'][3]
    print('with_height funcion -->', with_height[0:5])
    return with_height


def obtener_posiciones_nombres(first_array_band, text_zone):
    resultado = []
    '''
    Itero por cada first_array_band,name, separo por ' ' y busco si el nombre esta en la text_zone.text, cuando coincida guardo la posicion en first_array_band.img_zone devolviendo un array de objetos {name: '', band_id: '', img_zone: ''}
    '''
    for banda in first_array_band:
        full_name = banda['name']
        # Tomar solo la primera palabra
        first_word = full_name.split()[0]
        posicion_encontrada = None

        # Buscar la primera palabra en text_zone y guardar su posición si coincide
        for zona in text_zone:
            # Comparación sin importar mayúsculas
            if zona['text'].upper() == first_word.upper():
                posicion_encontrada = zona['position']
                # almaceno la posicion de text_zone
                indexStart = text_zone.index(zona)
                # itero apartir de la posicion encontrada para buscar el resto de la palabra y obtener el with de la suma de las palabras
                indexFinish = obtener_posicion_final(
                    full_name, text_zone, indexStart)
                with_height = obtener_with_height(
                    indexStart, indexFinish, text_zone)
                if len(with_height) >= 2:
                    # guardo la posicion final de la banda
                    posicion_encontrada = [
                        posicion_encontrada[0], posicion_encontrada[1], with_height[0], with_height[1]]
                else:
                    print(
                        "Error: with_height no tiene suficientes elementos", with_height)
                break
                break

        # Agregar el resultado con la posición de la primera palabra o None si no se encontró
        resultado.append({
            'name': banda['name'],
            'band_id': banda['band_id'],
            'img_zone': posicion_encontrada
        })
    print('text_zone -->', text_zone[0:5])
    print('resultado -->', resultado[0:5])
    # valido que devuelvo un array igual de largo que first_array_band
    if len(resultado) == len(first_array_band):
        return resultado
    else:
        print("Error en la longitud de los arrays",
              len(resultado), len(first_array_band))
        return
