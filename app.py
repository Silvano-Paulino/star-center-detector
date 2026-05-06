import cv2
import numpy as np
import pandas as pd
import streamlit as st
from detectort import processar_imagem_estrelas_v2


from detector import processar_imagem_estrelas

st.set_page_config(page_title="Star Center Detector", layout="wide")

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

    # Processar
    with st.spinner("A processar imagem..."):
        centros, img_resultado = processar_imagem_estrelas_v2(opencv_image)

    # Layout de colunas para exibir imagens
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagem Original")
        # OpenCV usa BGR, Streamlit/PIL usa RGB
        rgb_original = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
        st.image(rgb_original, width="stretch")

    with col2:
        st.subheader("Estrelas Detectadas")
        rgb_resultado = cv2.cvtColor(img_resultado, cv2.COLOR_BGR2RGB)
        st.image(rgb_resultado, width="stretch")

    # Exibir Lista de Coordenadas
    st.divider()
    st.subheader(f"📊 Coordenadas Detectadas ({len(centros)} estrelas)")

    if centros:
        # Criar DataFrame para manipulação de dados
        df = pd.DataFrame(centros, columns=["X (Pixel)", "Y (Pixel)"])
        df.insert(0, "ID", range(1, len(df) + 1))

        # Botão para baixar CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar Coordenadas (CSV)",
            data=csv,
            file_name="coordenadas_estrelas.csv",
            mime="text/csv",
        )

        # Exibir tabela no Streamlit
        st.table(df)

    else:
        st.warning(
            "Nenhuma estrela detectada. Tente ajustar o limiar ou use uma imagem com maior contraste."
        )
else:
    st.info("Aguardando upload de imagem...")
