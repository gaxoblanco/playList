import json
import re

# Subfunción para validar si una cadena tiene 2 o más espacios


def has_three_or_more_spaces(text):
    # Busca 2 o más espacios consecutivos en la cadena
    return len(re.findall(r' ', text)) >= 2


def detect_possible_errors(json_file):
    # Cargar los nombres del archivo JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            band_list = json.load(f)
    except FileNotFoundError:
        print(
            f"El archivo {json_file} no se encontró. Asegúrate de que el archivo existe y la ruta es correcta.")
        return
    except json.JSONDecodeError:
        print(
            f"Error al decodificar el archivo {json_file}. Asegúrate de que el archivo está bien formado.")
        return
    except UnicodeDecodeError:
        print(
            f"Error de codificación al leer el archivo {json_file}. Asegúrate de que el archivo está en formato UTF-8.")
        return

    # Patrones para dividir en partes (si coinciden se dividirán)
    error_patterns = [
        re.compile(r'La .*la', re.IGNORECASE),
        re.compile(r'la .*La', re.IGNORECASE),
        re.compile(r'la .*la ', re.IGNORECASE),
        re.compile(r'LA .*LA ', re.IGNORECASE),
        re.compile(r'El .*el', re.IGNORECASE),
        re.compile(r'el .*El', re.IGNORECASE),
        re.compile(r'el .*el ', re.IGNORECASE),
        re.compile(r'EL .*EL ', re.IGNORECASE),
        re.compile(r'Los .*los', re.IGNORECASE),
        re.compile(r'los .*Los', re.IGNORECASE),
        re.compile(r'los .*los ', re.IGNORECASE),
        re.compile(r'LOS .*LOS ', re.IGNORECASE),
        # posibles combinaciones de la, el, los
        re.compile(r'La .*los', re.IGNORECASE),
        re.compile(r'la .*Los', re.IGNORECASE),
        re.compile(r'La .*el', re.IGNORECASE),
        re.compile(r'la .*El', re.IGNORECASE),
        re.compile(r'Los .*la', re.IGNORECASE),
        re.compile(r'los .*La', re.IGNORECASE),
        re.compile(r'El .*los', re.IGNORECASE),
        re.compile(r'el .*Los', re.IGNORECASE),
        re.compile(r'El .*la', re.IGNORECASE),
        re.compile(r'el .*La', re.IGNORECASE),
        re.compile(r'Los .*el', re.IGNORECASE),
        re.compile(r'los .*El', re.IGNORECASE),
        re.compile(r'&'),  # "&" en el nombre
        re.compile(r' y ', re.IGNORECASE),
        re.compile(r' Y ', re.IGNORECASE),
        re.compile(r' x '),
        re.compile(r' X '),
        re.compile(r': '),
    ]

    # Nombres que tienen patrones problemáticos
    corrected_names = []

    for obj in band_list:
        name = obj['name']
        has_error = False

        # Verificar si algún patrón coincide con error_patterns
        for pattern in error_patterns:
            if pattern.search(name):
                has_error = True
                break

        # Verificar si la cadena tiene 3 o más espacios
        if has_three_or_more_spaces(name):
            has_error = True
            print(f"Nombre con 2 o más espacios detectado: {name}")

        if has_error:
            print(f"Nombre problemático encontrado: {name}")

            # Pedir al usuario ingresar el nombre correcto
            correct_name = input(
                "Ingrese el nombre correcto o deje vacío para mantener el actual: ").strip()

            # Si el usuario ingresa un nombre nuevo, actualizar
            if correct_name:
                obj['name'] = correct_name

            # Añadir la entrada corregida a la lista final
            corrected_names.append(obj)

            # Bucle para ingresar campos adicionales como nuevos elementos en el array
            while True:
                extra_field = input(
                    "Ingrese un valor adicional o deje vacío para finalizar: ").strip()
                if not extra_field:
                    break  # Si está vacío, salir del bucle
                # Crear un nuevo objeto con el valor adicional y añadirlo al array
                corrected_names.append({"name": extra_field, "band_id": ""})

        else:
            # Si no hay errores, añadir el objeto original
            corrected_names.append(obj)

    # Guardar los nombres corregidos en el archivo JSON
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(corrected_names, f, ensure_ascii=False, indent=4)

    print(f"Nombres corregidos guardados exitosamente en {json_file}")
