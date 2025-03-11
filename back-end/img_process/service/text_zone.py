import re
import pytesseract


def get_text_zones(img):
    """
    Detecta las zonas de texto en la imagen y devuelve información detallada.
    Filtra elementos que son solo caracteres especiales.
    """
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    zones = []

    # Filtramos elementos vacíos y caracteres especiales
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if text and not is_only_special_chars(text):
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            line_num = data['line_num'][i]
            block_num = data['block_num'][i]

            zones.append({
                'text': text,
                'position': (x, y, w, h),
                'line_num': line_num,
                'block_num': block_num
            })

    # Ordenamos por posición vertical (y) y luego horizontal (x)
    zones.sort(key=lambda z: (z['position'][1], z['position'][0]))
    return zones

# ---------


def is_only_special_chars(text):
    """
    Verifica si un texto contiene solo caracteres especiales, puntos o guiones.
    """
    pattern = r'^[^\w\s]+$'
    return re.match(pattern, text) is not None
