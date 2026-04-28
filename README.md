# ✨ Star Center Detector

Este projeto utiliza técnicas de Visão Computacional (OpenCV) para identificar automaticamente o centro de massa (centroides) de estrelas em imagens astronómicas.

## 🚀 Funcionalidades

- **Interface Web Interativa**: Carregamento de imagens via browser e visualização de resultados em tempo real.
- **Deteção Automática**: Algoritmo baseado em limiarização (thresholding) e momentos de imagem.
- **Exportação de Dados**: Lista detalhada de coordenadas (X, Y) das estrelas detetadas.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Pip (gestor de pacotes de Python)

## 🛠️ Instalação

Recomenda-se a utilização de um ambiente virtual para evitar conflitos de dependências:

1. **Criar o ambiente virtual:**

   ```bash
   python3 -m venv venv
   ```

   Nota>: No Windows, use `python` em vez de `python3`.
   Nota>: No NixOs, antes de executar o camando acima, execute `nix-shell` dentro da raiz do projecto.

2. **Ativar o ambiente:**
   - No Linux/macOS: `source venv/bin/activate`
   - No Windows: `venv\Scripts\activate`

3. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Como Utilizar

### Interface Web (Recomendado)

Para uma experiência visual completa:

```bash
streamlit run app.py
```

---

## ⚠️ Resolução de Problemas (Troubleshooting)

### Erro: `Segmentation fault (core dumped)` no Linux

Se encontrar este erro ao tentar correr o Streamlit no Linux (ex: Pop!\_OS ou Ubuntu), o problema deve-se geralmente a conflitos entre o OpenCV e as bibliotecas gráficas do sistema.

**Solução:**

1. Certifique-se de que está a usar a versão _headless_ do OpenCV no `requirements.txt`:
   ```text
   opencv-python-headless
   ```
2. Execute o Streamlit com a seguinte variável de ambiente:
   ```bash
   export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
   streamlit run app.py
   ```

## 📂 Estrutura do Projeto

- `app.py`: Interface Web utilizando Streamlit.
- `detector.py`: Módulo central com a lógica de processamento de imagem.
- `requirements.txt`: Lista de dependências do projeto.
- `pictures/`: Pasta para armazenamento de imagens de teste.
