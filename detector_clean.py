import os

import cv2
import numpy as np
import pandas as pd


def encontrar_centroides_clean(caminho_imagem):
    """
    Solução robusta e limpa para encontrar centros de estrelas.
    Utiliza limiarização adaptativa e componentes conectados.
    """
    if not os.path.exists(caminho_imagem):
        print(f"Erro: Imagem não encontrada.")
        return None

    # 1. Carregar a imagem
    img = cv2.imread(caminho_imagem)
    if img is None:
        return None

    # 2. Pré-processamento: Escala de cinza e Blur para suavizar ruído
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Limiarização Adaptativa (Lida com iluminação desigual na foto)
    # Ajustamos para pegar apenas os picos de brilho
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, -20
    )

    # 4. Encontrar componentes conectados (manchas de luz)
    # Esta função retorna o centroide (x, y) de cada mancha automaticamente
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

    centros = []
    for i in range(1, num_labels):  # Pular o fundo (label 0)
        area = stats[i, cv2.CC_STAT_AREA]

        # Filtro de área: Ignora ruído muito pequeno e manchas gigantescas
        if 5 < area < 5000:
            cx, cy = centroids[i]
            # Extrair brilho máximo da região para servir de referência
            x, y, w, h = (
                stats[i, cv2.CC_STAT_LEFT],
                stats[i, cv2.CC_STAT_TOP],
                stats[i, cv2.CC_STAT_WIDTH],
                stats[i, cv2.CC_STAT_HEIGHT],
            )
            roi = gray[y : y + h, x : x + w]
            peak = np.max(roi) if roi.size > 0 else 0

            centros.append(
                {
                    "x_centroid": int(np.round(cx)),
                    "y_centroid": int(np.round(cy)),
                    "area": area,
                    "peak": peak,
                }
            )

    df = pd.DataFrame(centros)
    return df, img


def main():
    imagem_alvo = "pictures/picture-2.jpeg"
    print(f"--- Iniciando Deteção Robusta (Centroides Clean) ---")

    resultado = encontrar_centroides_clean(imagem_alvo)

    if resultado:
        df, img = resultado
        if not df.empty:
            # Ordenar por brilho (pico) para mostrar as mais prováveis primeiro
            df = df.sort_values(by="peak", ascending=False)

            output_excel = "coordenadas_cientificas.xlsx"
            df[["x_centroid", "y_centroid", "peak", "area"]].to_excel(
                output_excel, index=False
            )

            print(f"Sucesso: {len(df)} estrelas detectadas.")
            print(f"Resultados guardados em {output_excel}")

            # Desenhar para validação
            for _, row in df.head(100).iterrows():  # Desenhar as 100 mais brilhantes
                cv2.drawMarker(
                    img,
                    (row["x_centroid"], row["y_centroid"]),
                    (0, 255, 0),
                    cv2.MARKER_CROSS,
                    20,
                    2,
                )

            # cv2.imwrite("validacao_clean.jpg", img)
        else:
            print("Nenhuma estrela encontrada.")


if __name__ == "__main__":
    main()
