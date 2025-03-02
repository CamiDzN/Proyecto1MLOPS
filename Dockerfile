FROM python:3.10-slim

# Instala curl para instalar uv
RUN apt-get update && apt-get install -y curl g++ libsnappy-dev 

# Instala uv y actualiza el PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Establece el directorio de trabajo
WORKDIR /workspace

# Inicializa un nuevo proyecto UV
RUN uv init proyecto1
WORKDIR /workspace/proyecto1

# Agrega las dependencias necesarias
RUN uv add requests tensorflow tfx google-api-python-client protobuf pandas tensorflow-data-validation scikit-learn uvicorn

# Instala Apache Beam con las dependencias interactivas manualmente
RUN pip install apache-beam[interactive] python-snappy

# (Opcional) Instala dependencias extras para la visualización interactiva
RUN pip install matplotlib bokeh ipywidgets

# Instala JupyterLab
RUN pip install jupyterlab

# Expone el puerto 8888 para JupyterLab
EXPOSE 8888

# Comando para iniciar JupyterLab
CMD ["sh", "-c", "uv run jupyter lab --ip=0.0.0.0 --allow-root --no-browser"]
