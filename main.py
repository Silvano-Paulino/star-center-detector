import os
import sys

import cv2
import numpy as np
import pandas as pd


def detectar_centro_estrelas_atraves_da_imagem(
    img,
    minDistValue=30,
    param1Value=50,
    param2Value=35,
    minRadiusValue=50,
    maxRadiusValue=100,
):
    """
    Versão Avançada (Hough): Utiliza a Transformada de Hough para detetar formas circulares.
    Útil para estrelas grandes, planetas ou imagens desfocadas.
    """
    if img is None:
        return [], None

    # 1. Pré-processamento
    if len(img.shape) == 3:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img

    # Suavizar para reduzir ruído (ajuda na deteção de círculos)
    suave = cv2.GaussianBlur(img_gray, (5, 5), 0)

    # 2. Aplicar a Transformada de Hough para Círculos
    circulos = cv2.HoughCircles(
        suave,
        cv2.HOUGH_GRADIENT,
        dp=1.0,
        minDist=minDistValue,
        param1=param1Value,
        param2=param2Value,
        minRadius=minRadiusValue,
        maxRadius=maxRadiusValue,
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
    # Caminho da imagem com validação
    caminho_imagem = "pictures/picture-2.jpeg"

    # Verificar se o arquivo existe
    if not os.path.exists(caminho_imagem):
        print(f"Erro: Arquivo não encontrado: {caminho_imagem}")
        print(f"Diretório atual: {os.getcwd()}")
        sys.exit(1)

    img = cv2.imread(caminho_imagem)

    if img is None:
        print(f"Erro: Não foi possível ler a imagem: {caminho_imagem}")
        sys.exit(1)

    centros, _ = detectar_centro_estrelas_atraves_da_imagem(img)
    print(f"Coordenadas encontradas: {len(centros)}")

    if centros:
        # Gerar DataFrame e exportar para Excel
        df = pd.DataFrame(centros, columns=["X", "Y"])
        nome_arquivo_excel = "./coordenadas_estrelas.xlsx"
        df.to_excel(nome_arquivo_excel, index=False, engine="openpyxl")
        print(f"Coordenadas exportadas para: {nome_arquivo_excel}")
    else:
        print("Nenhuma coordenada detectada.")

    # if resultado is not None:
    #     cv2.cvShowImage("Deteção V3 (Hough Circles)", resultado)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
