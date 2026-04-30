import cv2
import numpy as np


def processar_imagem_estrelas_v2(img):
    """
    Versão Standard: Utiliza Threshold fixo e Contornos do OpenCV.
    Ideal para rapidez e imagens com estrelas muito brilhantes.
    """
    if img is None:
        return [], None

    # 1. Converter para tons de cinza
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # 2. Aplicar um limiar (Threshold) para destacar as estrelas
    # O valor 200 isola apenas os pontos mais brilhantes
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # 3. Encontrar contornos das estrelas
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centros = []
    img_resultado = img.copy()

    # 4. Calcular o centro (momento) de cada contorno
    for c in contornos:
        M = cv2.moments(c)
        if M["m00"] != 0:
            # Cálculo das coordenadas X e Y do centroide
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centros.append((cx, cy))

            # Desenhar o centro na imagem de resultado
            cv2.circle(img_resultado, (cx, cy), 5, (0, 255, 0), -1)

    return centros, img_resultado


def main():
    # Mantém compatibilidade com script CLI
    caminho_imagem = "pictures/picture-1.jpeg"
    img = cv2.imread(caminho_imagem)

    if img is not None:
        centros, resultado = processar_imagem_estrelas_v2(img)
        print(f"Estrelas encontradas: {len(centros)}")
        cv2.imshow("Deteção V2 (Standard)", resultado)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
