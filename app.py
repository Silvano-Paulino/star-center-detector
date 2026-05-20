import io

import cv2
import numpy as np
import pandas as pd
import streamlit as st

# Importar os 3 detetores disponíveis
from detector import processar_imagem_estrelas
from detector_2 import processar_imagem_estrelas_v2
from detector_3 import processar_imagem_estrelas_v3

st.set_page_config(page_title="Star Center Detector", layout="wide")

# Configuração da Barra Lateral
st.sidebar.title("Configurações")
metodo = st.sidebar.selectbox(
    "Escolha o Algoritmo de Deteção:",
    ("Científico (DAOStarFinder)", "Standard (Momentos)", "Geométrico (Hough Circles)"),
)

st.sidebar.divider()
st.sidebar.info("""
**Dicas:**
- **Científico**: Melhor para precisão sub-pixel.
- **Standard**: Mais rápido para imagens claras.
- **Geométrico**: Útil para discos ou imagens desfocadas.
""")

st.title("✨ Star Center Detector")
st.markdown("""
Esta aplicação detecta automaticamente o centro de estrelas em imagens astronómicas.
Carregue a sua imagem abaixo para começar.
""")

uploaded_file = st.file_uploader(
    "Escolha uma imagem (JPG, PNG, TIFF)...", type=["jpg", "jpeg", "png", "tiff"]
)

if uploaded_file is not None:
    # Converter o ficheiro carregado para uma imagem OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Selecionar a função de processamento com base na escolha do utilizador
    if metodo == "Científico (DAOStarFinder)":
        funcao_deteccao = processar_imagem_estrelas
    elif metodo == "Standard (Momentos)":
        funcao_deteccao = processar_imagem_estrelas_v2
    else:
        funcao_deteccao = processar_imagem_estrelas_v3

    # Processar
    with st.spinner(f"A processar imagem com o método {metodo}..."):
        centros, img_resultado = funcao_deteccao(opencv_image)

    # Layout de colunas para exibir imagens
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagem Original")
        rgb_original = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
        st.image(rgb_original, use_container_width=True)

    with col2:
        st.subheader("Estrelas Detectadas")
        rgb_resultado = cv2.cvtColor(img_resultado, cv2.COLOR_BGR2RGB)
        st.image(rgb_resultado, use_container_width=True)

    # Exibir Lista de Coordenadas
    st.divider()
    st.subheader(f"📊 Coordenadas Detectadas ({len(centros)} estrelas)")

    if centros:
        # Criar DataFrame para manipulação de dados
        df = pd.DataFrame(centros, columns=["X (Pixel)", "Y (Pixel)"])
        df.insert(0, "ID", range(1, len(df) + 1))

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        st.download_button(
            label="📥 Baixar Coordenadas (XLSX)",
            data=buffer.getvalue(),
            file_name="coordenadas_estrelas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        # Exibir tabela no Streamlit
        st.table(df)

    else:
        st.warning(
            "Nenhuma estrela detectada. Tente ajustar o limiar ou use uma imagem com maior contraste."
        )
else:
    st.info("Aguardando upload de imagem...")
