import cv2

# Función para procesar la imagen (limpiar ruido y binarizar)


def preprocess_image(img):
    """
    Procesa la imagen para limpiarla (escala de grises, desenfoque y binarización).
    """
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro gaussiano para suavizar la imagen
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplicar binarización Otsu
    _, binary_img = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Mostrar la imagen binarizada
    # plt.imshow(binary_img, cmap='gray')
    # plt.axis('off')
    # plt.show()

    return binary_img  # Devuelve la imagen binarizada
