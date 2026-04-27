import cv2
from detector import processar_imagem_estrelas

def encontrar_centros_estrelas_cli(caminho_imagem):
    # 1. Carregar a imagem
    img = cv2.imread(caminho_imagem)

    if img is None:
        print("Erro ao carregar a imagem.")
        return

    # Usar o novo módulo de processamento
    centros, img_resultado = processar_imagem_estrelas(img)

    # Exibição original
    cv2.imshow("Estrelas Detectadas", img_resultado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return centros

def main():
    lista_coordenadas = encontrar_centros_estrelas_cli('./pictures/picture-1.jpg')
    print("Coordenadas detectadas:")
    for i, (x, y) in enumerate(lista_coordenadas):
        print(f"Estrela {i+1}: X={x}, Y={y}")

if __name__ == "__main__":
    main()
