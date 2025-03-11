import re


def extract_band_names(full_text):
    """
    Extrae nombres de bandas del texto completo OCR.
    Limpia y normaliza los separadores comunes en carteles de festivales.
    """
    # Convertimos a minúsculas para procesamiento
    text = full_text.lower()

    # Reemplazamos todos los separadores conocidos por saltos de línea
    separators = r'[+»«~*-.©¢_><;—]'
    text = re.sub(separators, '\n', text)

    # Dividimos por líneas y limpiamos
    lines = text.splitlines()
    bands = []

    for line in lines:
        line = line.strip()
        if line:
            # Eliminamos espacios múltiples
            line = re.sub(r'\s+', ' ', line)
            bands.append({"name": line, "band_id": ""})

    return bands
