import cv2


def encontrar_centros_estrelas(caminho_imagem):
    # 1. Carregar a imagem
    img = cv2.imread(caminho_imagem)
    if img is None:
        print("Erro ao carregar a imagem. Verifique o caminho.")
        return None

    # 2. Converter para tons de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Aplicar um limiar (Threshold) para destacar as estrelas
    # O valor 200 isola apenas os pontos mais brilhantes (0-255)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # 4. Encontrar contornos das estrelas
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centros = []

    # 5. Calcular o centro (momento) de cada contorno
    for c in contornos:
        M = cv2.moments(c)
        if M["m00"] != 0:
            # Cálculo das coordenadas X e Y do centroide
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            centros.append((cx, cy))

            # Desenhar o centro na imagem original para conferência
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), -1)

    # 6. Exibir o resultado visual
    cv2.imshow("Estrelas Detectadas", img)
    print(f"Estrelas encontradas: {len(centros)}")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return centros

def main():
    caminho_imagem = "pictures/picture-1.jpeg"  # Substitua pelo caminho da sua imagem
    centros = encontrar_centros_estrelas(caminho_imagem)

    print("Coordenadas dos centros das estrelas:")
    for idx, (x, y) in enumerate(centros):
        print(f"Estrela {idx + 1}: X={x}, Y={y}")

if __name__ == "__main__":
    main()