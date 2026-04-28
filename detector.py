import cv2
import numpy as np
from astropy.stats import sigma_clipped_stats
from photutils.detection import DAOStarFinder


def processar_imagem_estrelas(img):
    """
    Processa uma imagem de estrelas para detecção de centros..
    """
    if img is None:
        return [], None

    # 1. Converter para tons de cinza (Photutils trabalha com 2D arrays)
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Converter para float para cálculos astronómicos mais precisos
    data = gray.astype(np.float32)

    # 2. Estimar o Background (céu) e o ruído (ruído de leitura/disparo)
    # sigma_clipped_stats calcula média, mediana e desvio padrão ignorando outliers (estrelas)
    _, median, std = sigma_clipped_stats(data, sigma=3.0)

    # 3. Configurar o Finder (DAOStarFinder)
    # fwhm: Full Width at Half Maximum (largura aproximada da estrela em pixels)
    # threshold: Deteção de objetos 5 sigmas acima do ruído de fundo
    daofind = DAOStarFinder(fwhm=3.0, threshold=5.0 * std)

    # Executar a deteção (subtraindo a mediana do fundo para isolar as estrelas)
    sources = daofind(data - median)

    centros = []
    img_resultado = img.copy()

    if sources is not None:
        for col in sources:
            x = float(col["x_centroid"])
            y = float(col["y_centroid"])
            centros.append((x, y))

            # Desenhar na imagem (OpenCV precisa de ints para desenhar o círculo)
            cv2.circle(img_resultado, (int(x), int(y)), 5, (0, 255, 0), -1)

    return centros, img_resultado
