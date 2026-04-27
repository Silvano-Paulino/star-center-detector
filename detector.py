import cv2
import numpy as np

def processar_imagem_estrelas(img):
    """
    Recebe uma imagem (numpy array), detecta estrelas e retorna os centros
    e a imagem com os centros desenhados.
    """
    if img is None:
        return [], None

    # 1. Converter para tons de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. Aplicar um limiar (Threshold) para destacar as estrelas
    # Valor fixo de 200 conforme o código original
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # 3. Encontrar contornos das estrelas
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centros = []
    # Criar uma cópia para não alterar a original se necessário
    img_resultado = img.copy()

    for c in contornos:
        M = cv2.moments(c)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centros.append((cx, cy))
            # Desenhar o centro na imagem de resultado
            cv2.circle(img_resultado, (cx, cy), 5, (0, 255, 0), -1)

    return centros, img_resultado
