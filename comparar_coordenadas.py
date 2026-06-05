import os
import re

import numpy as np
import pandas as pd


def extrair_coordenadas_md(caminho_md):
    """
    Extrai as coordenadas X e Y do ficheiro markdown coordenadas-estrelas-scan.md
    """
    with open(caminho_md, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex para capturar as linhas da tabela: | No | X | Y | ...
    # Exemplo: | 1 | 1635 | 2053 | -669 | -325 | 258,8 |
    pattern = r"\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|"
    matches = re.findall(pattern, content)

    if not matches:
        print("Aviso: Nenhuma coordenada encontrada no ficheiro MD.")
        return pd.DataFrame(columns=["No", "X_manual", "Y_manual"])

    df = pd.DataFrame(matches, columns=["No", "X_manual", "Y_manual"])
    df["X_manual"] = df["X_manual"].astype(float)
    df["Y_manual"] = df["Y_manual"].astype(float)
    return df


def comparar(df_manual, df_cientifico, tolerancia=10):
    """
    Compara as coordenadas manuais com as detectadas pelo DAOStarFinder.
    tolerancia: distância máxima em pixels para considerar a mesma estrela.
    """
    print(f"Cruzando dados (Tolerância: {tolerancia} pixels)...")

    correspondencias = []

    for i, manual in df_manual.iterrows():
        # Calcular distância euclidiana para todos os pontos detectados
        distancias = np.sqrt(
            (df_cientifico["x_centroid"] - manual["X_manual"]) ** 2
            + (df_cientifico["y_centroid"] - manual["Y_manual"]) ** 2
        )

        idx_min = distancias.idxmin()
        if distancias[idx_min] <= tolerancia:
            correspondencias.append(
                {
                    "No": manual["No"],
                    "X_manual": manual["X_manual"],
                    "Y_manual": manual["Y_manual"],
                    "x_centroid": df_cientifico.loc[idx_min, "x_centroid"],
                    "y_centroid": df_cientifico.loc[idx_min, "y_centroid"],
                    "Erro_Pixels": distancias[idx_min],
                    "Status": "Encontrada",
                }
            )

        else:
            correspondencias.append(
                {
                    "No": manual["No"],
                    "X_manual": manual["X_manual"],
                    "Y_manual": manual["Y_manual"],
                    "Status": "Não Encontrada",
                }
            )

    df_comp = pd.DataFrame(correspondencias)

    # Identificar estrelas "Novas" (que estão no científico mas não no manual)
    detectadas_indices = []
    for c in correspondencias:
        if c["Status"] == "Encontrada":
            # Encontrar o index original no df_cientifico
            idx = df_cientifico[
                (df_cientifico["x_centroid"] == c["x_centroid"])
                & (df_cientifico["y_centroid"] == c["y_centroid"])
            ].index
            detectadas_indices.extend(idx.tolist())

    novas_estrelas = df_cientifico.drop(index=detectadas_indices)

    return df_comp, novas_estrelas


def main():
    path_md = "coordenadas-estrelas-scan.md"
    path_xlsx = "coordenadas_cientificas.xlsx"

    if not os.path.exists(path_xlsx):
        print(
            f"Erro: Ficheiro {path_xlsx} não encontrado. Corre primeiro o 'detector_cientifico.py'."
        )
        return

    print("--- Iniciando Comparação de Dados ---")

    # 1. Carregar dados
    df_manual = extrair_coordenadas_md(path_md)
    df_cientifico = pd.read_excel(path_xlsx)

    # 2. Executar comparação
    df_resultado, df_novas = comparar(df_manual, df_cientifico)

    # 3. Mostrar Resumo
    encontradas = len(df_resultado[df_resultado["Status"] == "Encontrada"])
    total_manual = len(df_manual)
    total_novas = len(df_novas)

    print("\nRESUMO:")
    print(f"- Estrelas do Scan: {total_manual}")
    print(
        f"- Encontradas pelo Algoritmo: {encontradas} ({(encontradas / total_manual) * 100:.1f}%)"
    )
    print(f"- Novas Estrelas detetadas (não estavam no scan): {total_novas}")

    # 4. Salvar Relatório
    output_path = "relatorio_comparacao.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        df_resultado.to_excel(writer, sheet_name="Comparação", index=False)
        df_novas.to_excel(writer, sheet_name="Novas Estrelas", index=False)

    print(f"\nRelatório detalhado guardado em: {output_path}")


if __name__ == "__main__":
    main()
