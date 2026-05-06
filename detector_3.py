import cv2
import numpy as np


def detectar_centros(caminho_imagem):
    # 1. Carregar a imagem
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        print("Erro ao carregar a imagem.")
        return

    # 2. Pré-processamento
    # Converter para escala de cinza
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Suavizar para reduzir ruído (ajuda na deteção)
    suave = cv2.medianBlur(cinza, 5)

    # 3. Aplicar a Transformada de Hough para Círculos
    # Parâmetros: imagem, método, dp, dist_min_centros, param1(bordas), param2(precisão), minRadius, maxRadius
    circulos = cv2.HoughCircles(
        suave,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=30,
        param1=50,
        param2=35,
        minRadius=10,
        maxRadius=150,
    )

    # 4. Processar resultados
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))

        print(f"Encontradas {len(circulos[0])} manchas:")

        for i in circulos[0, :]:
            centro_x, centro_y, raio = i[0], i[1], i[2]

            # Imprimir coordenadas
            print(f"Centro: X={centro_x}, Y={centro_y} | Raio={raio}")

            # Desenhar na imagem para visualização
            cv2.circle(imagem, (centro_x, centro_y), raio, (0, 255, 0), 2)  # Círculo
            cv2.circle(imagem, (centro_x, centro_y), 2, (0, 0, 255), 3)  # Centro

        # Mostrar imagem final
        cv2.imshow("Deteção de Manchas", imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Nenhum círculo detetado. Tenta ajustar os parâmetros param1 ou param2.")


def main():
    detectar_centros("pictures/picture-1.jpeg")


if __name__ == "__main__":
    main()
