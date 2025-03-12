def create_error_response(error_type, normalized_name, original_name):
    """Crea una respuesta de error estandarizada."""
    return {
        'id': f"-{error_type}-{normalized_name}",
        'img': "img_error",
        'genres': [],
        'name': original_name,
        'popularity': 0
    }
