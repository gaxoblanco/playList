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


def obtener_posiciones_nombres(first_array_band, text_zone):
    resultado = []
    '''
    Itero por cada first_array_band,name, separo por ' ' y busco si el nombre esta en la text_zone.text, cuando coincida guardo la posicion en first_array_band.img_zone devolviendo un array de objetos {name: '', band_id: '', img_zone: ''}
    '''
    for banda in first_array_band:
        nombre_completo = banda['name']
        # Tomar solo la primera palabra
        primera_palabra = nombre_completo.split()[0]
        posicion_encontrada = None

        # Buscar la primera palabra en text_zone y guardar su posición si coincide
        for zona in text_zone:
            # Comparación sin importar mayúsculas
            if zona['text'].upper() == primera_palabra.upper():
                posicion_encontrada = zona['position']
                break

        # Agregar el resultado con la posición de la primera palabra o None si no se encontró
        resultado.append({
            'name': banda['name'],
            'band_id': banda['band_id'],
            'img_zone': posicion_encontrada
        })

    # valido que devuelvo un array igual de largo que first_array_band
    if len(resultado) == len(first_array_band):
        return resultado
    else:
        print("Error en la longitud de los arrays",
              len(resultado), len(first_array_band))
        return
