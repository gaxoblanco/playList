
import warnings


def validate_status_code(status_code, result, band_item, spotify_data, band_name):
    # Si se añadió correctamente o ya existía
    if status_code in [201, 409]:
        # Actualizar el item con datos de Spotify
        band_item['band_id'] = spotify_data['id']
        band_item['name'] = spotify_data.get('name', '')
        band_item['img_url'] = spotify_data.get('img', '')
        band_item['popularity'] = spotify_data.get('popularity', 0)
        band_item['genres'] = spotify_data.get('genres', [])

        # Si la banda ya existía, obtenemos su ID de la base de datos
        if status_code == 409 and 'id' in result:
            warnings.warn(
                f"Banda '{band_name} - {spotify_data.get('name')}' ya existe en la base de datos.")

        print("Banda añadida:", band_item)
        return band_item
    else:
        # Si hubo un error al añadir, añadimos solo lo que tenemos
        band_item['error'] = "No se pudo guardar en la base de datos"
        return band_item
