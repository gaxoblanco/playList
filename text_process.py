# json
import re
import json


def extract_names(response_text):
    # Paso 1: Detectar los separadores no alfabéticos
    # Detecta patrones como \cdot y otros
    separators = re.findall(r'(\\[a-z]+|\W+)', response_text)
    if not separators:
        print("No separators found!")
        return []

    # Paso 2: Mostrar los separadores detectados al usuario
    print("Separadores detectados: ", set(separators))

    # Pedir al usuario que ingrese el separador, o usar el más común si no se ingresa nada
    user_separator = input(
        "Ingrese el separador que desea usar (deje vacío para usar el más común): ")

    if user_separator.strip():
        most_common_separator = user_separator.strip()
    else:
        # Si el usuario no ingresa nada, usar el separador más repetido
        separator_counts = {}
        for separator in separators:
            if len(separator) > 1:  # Asegurarse de que el separador tiene más de 1 carácter
                separator_counts[separator] = separator_counts.get(
                    separator, 0) + 1

        most_common_separator = max(
            separator_counts, key=separator_counts.get, default='')  # type: ignore
        if not most_common_separator:
            print("No separator found!")
            return []

    # Paso 3: Usar el separador más común para dividir los nombres
    names = response_text.split(most_common_separator)

    # Retornar los nombres y el separador más común
    return names


# Función para guardar los nombres como objetos en un archivo JSON
def save_to_json(names):
    # Preguntar al usuario por el nombre del archivo
    file_name = input(
        "Ingrese el nombre del archivo JSON (sin extensión): ") + '.json'

    # Crear una lista de objetos, donde cada objeto contiene el nombre y el campo band_id vacío
    names_objects = [{"name": name, "band_id": ""} for name in names]

    # Guardar los objetos en un archivo JSON
    with open(file_name, 'w') as f:
        json.dump(names_objects, f, ensure_ascii=False, indent=4)

    print(f"Nombres guardados exitosamente en {file_name}")
