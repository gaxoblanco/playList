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
    return names, most_common_separator


def save_to_json(names, file_name='names.json'):
    # Paso 4: Guardar los nombres en un archivo JSON
    with open(file_name, 'w') as f:
        json.dump(names, f, ensure_ascii=False, indent=4)
    print(f"Saved names to {file_name}")


# Ejemplo de salida del modelo
response = "OLIVIA RODRIGO \cdot JUSTIN TIMBERLAKE \cdot SHAWN MENDES \cdot ALANIS MORISSETTE"

# Extraer nombres y guardarlos en un JSON
# names = extract_names(response)
# print("Extracted names:", names)

# save_to_json(names)
