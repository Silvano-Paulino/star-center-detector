import os

import cv2
import numpy as np
import pandas as pd
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder


def detectar_estrelas_momentos(img, threshold_value=200):
    """
    Método robusto para estrelas grandes: usa binarização e centros de massa.
    Ideal quando o DAOStarFinder falha por causa de saturação ou tamanho.
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Aplicar threshold para isolar o brilho das estrelas
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Encontrar contornos
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centros = []
    for c in contornos:
        M = cv2.moments(c)
        if M["m00"] > 10:  # Filtro de área mínima
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centros.append(
                {
                    "x_centroid": cx,
                    "y_centroid": cy,
                    "peak": np.max(gray[c[:, :, 1], c[:, :, 0]]) if len(c) > 0 else 0,
                }
            )

    return pd.DataFrame(centros)


def detectar_estrelas_dao(caminho_imagem, fwhm=30.0, threshold_sigma=3.0):
    """
    Detecta estrelas usando o algoritmo DAOStarFinder.
    Reduzido FWHM para 30 para focar no núcleo (peak) da estrela.
    """
    if not os.path.exists(caminho_imagem):
        print(f"Erro: Imagem não encontrada em {caminho_imagem}")
        return None

    # 1. Carregar a imagem
    img = cv2.imread(caminho_imagem)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem {caminho_imagem}")
        return None

    # 2. Converter para escala de cinza (DAO trabalha com 2D)
    if len(img.shape) == 3:
        data = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float)
    else:
        data = img.astype(float)

    # 3. Calcular estatísticas do fundo (background) para remover ruído
    mean, median, std = sigma_clipped_stats(data, sigma=3.0)

    # 4. Configurar o DAOStarFinder
    # fwhm: Full Width at Half Maximum (largura média das estrelas em pixels)
    # threshold: nível acima do fundo para considerar uma estrela
    daofind = DAOStarFinder(fwhm=fwhm, threshold=threshold_sigma * std)

    # 5. Executar a deteção
    sources = daofind(data - median)

    if sources is None:
        print("Nenhuma estrela detectada com os parâmetros atuais.")
        return None

    # 6. Converter resultados para DataFrame
    df_detectado = sources.to_pandas()

    # Converter para inteiros (arredondando para o mais próximo)
    df_detectado["x_centroid"] = np.round(df_detectado["x_centroid"]).astype(int)
    df_detectado["y_centroid"] = np.round(df_detectado["y_centroid"]).astype(int)

    print(f"Deteção concluída: {len(df_detectado)} estrelas encontradas.")
    return df_detectado, img


def main():
    imagem_alvo = "pictures/picture-2.jpeg"
    print(
        f"--- Iniciando Deteção por Momentos (Estrelas Grandes) em: {imagem_alvo} ---"
    )

    # 1. Carregar imagem
    img = cv2.imread(imagem_alvo)
    if img is None:
        print(f"Erro: Não foi possível carregar a imagem {imagem_alvo}")
        return

    # 2. Executar deteção por Momentos
    # threshold_value=200 é um bom ponto de partida para estrelas brilhantes
    df = detectar_estrelas_momentos(img, threshold_value=150)

    if not df.empty:
        # Garantir coordenadas inteiras (já são int no método de momentos, mas reforçamos)
        df["x_centroid"] = df["x_centroid"].astype(int)
        df["y_centroid"] = df["y_centroid"].astype(int)

        # Guardar resultados
        output_excel = "coordenadas_cientificas.xlsx"
        # O método de momentos não gera 'mag', por isso usamos o 'peak' como referência
        df[["x_centroid", "y_centroid", "peak"]].to_excel(output_excel, index=False)
        print(f"Deteção concluída: {len(df)} estrelas encontradas.")
        print(f"Resultados exportados para {output_excel}")

        # Opcional: Desenhar na imagem para validação visual
        for index, row in df.iterrows():
            cv2.circle(img, (row["x_centroid"], row["y_centroid"]), 15, (0, 255, 0), 2)

        # cv2.imwrite("deteccao_momentos_validacao.jpg", img)
    else:
        print("Nenhuma estrela detectada com o método de momentos.")


if __name__ == "__main__":
    main()
