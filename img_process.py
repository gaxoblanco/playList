"""
URL para ejecutar en Google Colab
https://colab.research.google.com/drive/1FGmweUe0OwhugPHz9o5vxXF3dZc2DLG9#scrollTo=ina9caf2L3YV
"""

import torch
from transformers import AutoModelForCausalLM, AutoProcessor, BitsAndBytesConfig
from PIL import Image

# Verificar si la GPU está disponible y seleccionar dispositivo
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Mostrar si está usando GPU o CPU
print(f"Using device: {DEVICE}")

# Cargar el modelo
model_id = "yifeihu/TB-OCR-preview-0.1"

if torch.cuda.is_available():
    # Si hay GPU disponible, carga el modelo en 4 bits
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype="auto"  # No usar 4-bit, solo cargar el modelo con soporte de GPU
    )
else:
    # Si no hay GPU, cargar el modelo en la CPU sin cuantización
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        trust_remote_code=True,
        torch_dtype="auto"
    )

# Cargar el procesador asociado al modelo
processor = AutoProcessor.from_pretrained(model_id,
                                          trust_remote_code=True,
                                          num_crops=16
                                          )

# Función ajustada para cargar una imagen local


def phi_ocr(image_path):
    question = "Convert the text to markdown format."  # Instrucción para el modelo
    image = Image.open(image_path)  # Cargar la imagen desde una ruta local
    prompt_message = [{
        'role': 'user',
        'content': f'<|image_1|>\n{question}',
    }]

    # Generar el prompt y procesar la imagen
    prompt = processor.tokenizer.apply_chat_template(
        prompt_message, tokenize=False, add_generation_prompt=True)
    inputs = processor(prompt, [image], return_tensors="pt").to(DEVICE)

    # Configurar los argumentos de generación
    generation_args = {
        "max_new_tokens": 1024,
        "temperature": 0.1,
        "do_sample": False
    }

    # Generar la salida del modelo
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


# Llamar a la función con la imagen local
image_path = "banda.jpg"  # Asegúrate de que la imagen esté en la misma carpeta
response = phi_ocr(image_path)

# Imprimir la respuesta procesada
print(response)
