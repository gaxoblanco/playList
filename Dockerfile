# Usar una imagen base
FROM python:3.10-slim

# Instalar dependencias del sistema, incluyendo libGL
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    tesseract-ocr \
    libtesseract-dev \
    build-essential \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el c�digo
COPY . /app

# Dar permisos al directorio de la aplicación
RUN chmod -R 755 /app

# Cambiar a python app.py para desarrollo
CMD ["python", "app.py"]