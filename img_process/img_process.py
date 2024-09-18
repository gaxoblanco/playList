"""
URL para ejecutar en Google Colab
https://colab.research.google.com/drive/1FGmweUe0OwhugPHz9o5vxXF3dZc2DLG9#scrollTo=ina9caf2L3YV

---
Pruevas con modelos alternativos:
https://colab.research.google.com/drive/1GTFNNSmMu0WlWkn8vDu8LdMKC9p4Flsz#scrollTo=3toc2Xtdqk-v
"""
from PIL import Image
from transformers import AutoModelForCausalLM, AutoProcessor
import json
import torch
from accelerate import Accelerator


from list_img import listar_imagenes, resize_image
from extract_names import extract_names

# Verificar si la GPU está disponible y seleccionar dispositivo
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Mostrar si está usando GPU o CPU
print(f"Using device: {DEVICE}")

# Inicializar Accelerator
accelerator = Accelerator()

# Cargar el modelo
model_id = "yifeihu/TB-OCR-preview-0.1"
model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
processor = AutoProcessor.from_pretrained(model_id, trust_remote_code=True)
# Preparar el modelo para Accelerator
model = accelerator.prepare(model)
# Asegurarse de que el procesador también esté en el dispositivo adecuado
processor = processor.to(accelerator.device)

# Verificar el dispositivo de trabajo
print(f"Using device: {accelerator.device}")

# ----
# # consultar al usuario si usar GPU o CPU
# print("Seleccione el dispositivo para cargar el modelo:")
# print("1. GPU")
# print("2. CPU")
# device_option = input("Ingrese el número de la opción deseada: ")


# if device_option == '1' and torch.cuda.is_available():
#     model = AutoModelForCausalLM.from_pretrained(
#         model_id,
#         device_map="auto",
#         torch_dtype=torch.float16,  # Usar float16 para reducir el uso de memoria
#         trust_remote_code=True
#     )
# else:
#     # Si no hay GPU, cargar el modelo en la CPU sin cuantización
#     model = AutoModelForCausalLM.from_pretrained(
#         model_id,
#         trust_remote_code=True,
#         torch_dtype="auto"
#     )

# Cargar el procesador asociado al modelo
processor = AutoProcessor.from_pretrained(model_id,
                                          trust_remote_code=True,
                                          num_crops=16
                                          )

#

# Función para procesar la imagen y extraer el texto


def phi_ocr(image_path):

    question = "Convert the text to markdown format."
    image = Image.open(image_path)
    prompt_message = [{
        'role': 'user',
        'content': f'<|image_1|>\n{question}',
    }]

    image = resize_image(image_path, max_size=(524, 524))

    # Generar el prompt y procesar la imagen
    prompt = processor.tokenizer.apply_chat_template(
        prompt_message, tokenize=False, add_generation_prompt=True)
    inputs = processor(prompt, [image], return_tensors="pt").to(
        accelerator.device)

    # Configurar los argumentos de generación
    generation_args = {
        "max_new_tokens": 1024,
        "temperature": 0.1,
        "do_sample": False
    }

    # Generar la salida del modelo
    with torch.no_grad():
        generate_ids = model.generate(
            **inputs, eos_token_id=processor.tokenizer.eos_token_id, **generation_args)

    # Quitar los tokens de entrada de los resultados generados
    generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]

    # Decodificar el resultado generado
    response = processor.batch_decode(
        generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

    # Limpiar el resultado quitando el token de fin de imagen
    response = response.split("<image_end>")[0]

    return response


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


# Consultar al usuario si desea subir una imagen o no, y procesarla si se sube
uploaded = {}
upload_image = input("¿Desea subir una imagen para procesar? (s/n): ")

# Busco la imagen en el directorio local y la subo a la carpeta de trabajo // ya no uso colab
if upload_image.lower() == 's':
    # image_path = input("Ingrese la ruta de la imagen: ")
    image_path = "img/ocr_test_1.png"

    uploaded[image_path] = image_path
else:
    # Consultar al usuario con qué imagen desea trabajar dentro de las disponibles en el directorio
    imagen_elegida = listar_imagenes()
    if imagen_elegida:
        uploaded[imagen_elegida] = imagen_elegida


# Procesar la imagen subida
for filename in uploaded.keys():
    try:
        response = phi_ocr(filename)
        print(f"Response for {filename}:\n", response)

        # Extraer nombres de la respuesta
        names = extract_names(response)
        print("Extracted Names:", names)

        # Guardar los nombres en un archivo JSON
        save_to_json(names)

    except Exception as e:
        print(f"Error al procesar la imagen {filename}: {str(e)}")
