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
