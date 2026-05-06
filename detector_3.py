import cv2
import numpy as np


def processar_imagem_estrelas_v3(img):
    """
    Versão Avançada (Hough): Utiliza a Transformada de Hough para detetar formas circulares.
    Útil para estrelas grandes, planetas ou imagens desfocadas.
    """
    if img is None:
        return [], None

    # 1. Pré-processamento
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Suavizar para reduzir ruído (ajuda na deteção de círculos)
    suave = cv2.medianBlur(gray, 5)

    # 2. Aplicar a Transformada de Hough para Círculos
    # dp=1.2, minDist=30, param1=50, param2=35, minRadius=10, maxRadius=150
    circulos = cv2.HoughCircles(
        suave,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=30,
        param1=50,
        param2=35,
        minRadius=10,
        maxRadius=150,
    )

    centros = []
    img_resultado = img.copy()

    # 3. Processar resultados
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        for i in circulos[0, :]:
            cx, cy, raio = int(i[0]), int(i[1]), int(i[2])
            centros.append((cx, cy))

            # Desenhar o círculo e o centro na imagem de resultado
            cv2.circle(img_resultado, (cx, cy), raio, (0, 255, 0), 2)  # Contorno
            cv2.circle(img_resultado, (cx, cy), 2, (0, 0, 255), 3)  # Centro

    return centros, img_resultado


def main():
    # Mantém compatibilidade com script CLI
    caminho_imagem = "pictures/picture-1.jpeg"
    img = cv2.imread(caminho_imagem)

    if img is not None:
        centros, resultado = processar_imagem_estrelas_v3(img)
        print(f"Manchas encontradas: {len(centros)}")
        cv2.imshow("Deteção V3 (Hough Circles)", resultado)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
