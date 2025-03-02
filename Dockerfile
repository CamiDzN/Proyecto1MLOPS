FROM python:3.10

RUN apt-get update && apt-get install -y curl g++ 

RUN mkdir /workspace

# Establece el directorio de trabajo
WORKDIR /workspace

# Copiar el archivo de requisitos al contenedor
COPY requirements.txt ./

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

RUN pip install apache-beam[interactive]

RUN pip install jupyterlab

# Expone el puerto 8888 para JupyterLab
EXPOSE 8888

# Comando para iniciar JupyterLab
#CMD ["sh", "-c", "uv run jupyter lab --ip=0.0.0.0 --allow-root --no-browser"]
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
