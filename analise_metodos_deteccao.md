# Análise Comparativa de Métodos de Deteção de Estrelas

Este documento detalha a eficácia de diferentes algoritmos de visão computacional aplicados à localização de centros estelares, com foco especial na comparação entre a Transformada de Hough e métodos de Intensidade/Momentos.

---

## 1. Transformada de Hough (`cv2.HoughCircles`)

A Transformada de Hough é um método clássico para detetar formas geométricas parametrizadas.

### Por que NÃO é recomendado para estrelas:
*   **Geometria vs. Intensidade:** O Hough procura por gradientes de borda que formam um arco. Estrelas são picos de luz (PSF - Point Spread Function) e não discos sólidos com bordas definidas.
*   **Escala e Resolução:** Parâmetros como `minRadius` tornam o algoritmo cego para estrelas pequenas (pontuais), que são a maioria em imagens astronómicas.
*   **Falsos Positivos:** Para detetar círculos muito pequenos, a sensibilidade precisa de ser tão alta que o ruído digital da câmara é frequentemente confundido com estrelas.
*   **Complexidade de Calibração:** Exige o ajuste de múltiplos parâmetros (`dp`, `param1`, `param2`, `minDist`) que variam drasticamente conforme a câmara e a lente.

---

## 2. Threshold + Momentos (Método Standard / `detector-2.py`)

Este método binariza a imagem e calcula o centro de massa da mancha de luz.

### Vantagens:
*   **Velocidade:** É o método mais rápido computacionalmente.
*   **Flexibilidade:** Deteta qualquer mancha de luz, independentemente de ser um círculo perfeito ou uma estrela ligeiramente alongada (devido ao movimento da Terra, por exemplo).
*   **Robustez de Escala:** Funciona bem em resoluções de 16MP a 500MP sem grandes alterações de lógica.

---

## 3. DAOStarFinder / Photutils (Método Científico / `detector.py`)

Baseado em modelos matemáticos de distribuição de luz estelar.

### Vantagens:
*   **Precisão Sub-pixel:** Consegue determinar o centro da estrela com precisão de frações de pixel (ex: 10.42).
*   **Deteção em Ruído:** Consegue isolar estrelas muito fracas que mal se distinguem do fundo do céu através de análise estatística (`sigma_clipped_stats`).
*   **Padrão de Astronomia:** É o método utilizado em observatórios profissionais.

---

## Tabela Comparativa

| Critério | Hough Circles | Threshold + Momentos | DAOStarFinder |
| :--- | :--- | :--- | :--- |
| **Precisão** | Baixa | Média | **Altíssima** |
| **Velocidade** | Lenta | **Instantânea** | Média |
| **Facilidade de Uso** | Difícil | **Fácil** | Média |
| **Uso Ideal** | Discos planetários ou desfocagem | Protótipos e visualização | **Ciência e Astrometria** |

## Conclusão e Recomendação

Para o projeto **Star Center Detector**, os métodos baseados em **Intensidade (Momentos ou DAOStarFinder)** são superiores. A Transformada de Hough, embora poderosa para objetos industriais ou moedas, falha em capturar a natureza física da luz estelar, resultando em perda de dados e baixa precisão em imagens de alta resolução.
