import random
from typing import Dict, Callable, List, Any, Union, Tuple
from .get_top_three_popular_genres import get_top_three_popular_genres
from .get_least_popular_genre import get_least_popular_genre


def generet_random_info(db_session):
    """
    Genera información aleatoria eligiendo una de las funciones disponibles
    y ejecutándola con la sesión de base de datos proporcionada.

    Args:
        db_session: La sesión de base de datos a utilizar

    Returns:
        Un diccionario con el formato {'1': 'texto...'} que es el resultado de la función ejecutada
    """
    # Definir funciones que recibirán la sesión de base de datos
    def get_top_genres():
        return get_top_three_popular_genres(db_session)

    def get_least_genre():
        return get_least_popular_genre(db_session)

    # Crear el diccionario de funciones
    info_functions = {
        'top_genre': get_top_genres,
        'least_genre': get_least_genre
        # Puedes agregar más funciones aquí
    }

    # Usar information_loading para obtener un resultado aleatorio
    return information_loading(info_functions)


def information_loading(functions_dict: Dict[str, Callable[[], Dict[str, str]]]) -> Dict[str, str]:
    """
    Selecciona aleatoriamente una clave del diccionario proporcionado y ejecuta
    la función asociada a esa clave, devolviendo el resultado.

    Args:
        functions_dict: Un diccionario donde las claves son identificadores y los valores
                       son funciones que retornan un diccionario con formato {'1': 'texto...'}

    Returns:
        Un diccionario con el formato {'1': 'texto...'} que es el resultado de la función ejecutada
    """
    if not functions_dict:
        return {'1': 'No hay información disponible'}

    # Seleccionar una clave aleatoria del diccionario
    random_key = random.choice(list(functions_dict.keys()))

    # Obtener la función asociada a la clave
    function_to_execute = functions_dict[random_key]

    try:
        # Ejecutar la función y obtener el resultado
        result = function_to_execute()

        # Verificar que el resultado tenga el formato esperado
        if not isinstance(result, dict) or not result:
            return {'1': f'Error: La función {random_key} no devolvió un diccionario válido'}

        return result
    except Exception as e:
        # Manejar cualquier error que pueda ocurrir durante la ejecución
        return {'1': f'Error al ejecutar la función {random_key}: {str(e)}'}
