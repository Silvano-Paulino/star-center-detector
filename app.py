import streamlit as st
import cv2
import numpy as np
from detector import processar_imagem_estrelas

st.set_page_config(page_title="Star Center Detector", layout="wide")

st.title("✨ Star Center Detector")
st.markdown("""
Esta aplicação detecta automaticamente o centro de estrelas em imagens astronómicas.
Carregue a sua imagem abaixo para começar.
""")

uploaded_file = st.file_uploader("Escolha uma imagem (JPG, PNG, TIFF)...", type=["jpg", "jpeg", "png", "tiff"])

if uploaded_file is not None:
    # Converter o ficheiro carregado para uma imagem OpenCV
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Processar
    with st.spinner('A processar imagem...'):
        centros, img_resultado = processar_imagem_estrelas(opencv_image)

    # Layout de colunas para exibir imagens
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagem Original")
        # OpenCV usa BGR, Streamlit/PIL usa RGB
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
        # Criar uma tabela formatada
        dados_tabela = [{"ID": i+1, "X (Pixel)": c[0], "Y (Pixel)": c[1]} for i, c in enumerate(centros)]
        st.table(dados_tabela)
    else:
        st.warning("Nenhuma estrela detectada. Tente ajustar o limiar ou use uma imagem com maior contraste.")
else:
    st.info("Aguardando upload de imagem...")
