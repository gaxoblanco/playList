import unicodedata


def normalize_band_name(band_name):
    """Normaliza nombres para una comparación más precisa"""
    # Normalizar el nombre de la banda a minúsculas y eliminar caracteres especiales
    band_name = band_name.strip().lower()
    band_name = unicodedata.normalize('NFKD', band_name).encode(
        'ASCII', 'ignore').decode('ASCII')

    # Eliminar caracteres no alfanuméricos y espacios múltiples
    band_name = ''.join(c for c in band_name if c.isalnum() or c.isspace())
    band_name = ' '.join(band_name.split())
    return band_name
