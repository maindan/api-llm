FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Define o diretório de trabalho UM NÍVEL ACIMA
WORKDIR /src

# Copia o requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a pasta 'app' para dentro de '/src/app'
COPY ./app ./app

# Define o PYTHONPATH para /src
ENV PYTHONPATH=/src

# No docker-compose, o comando precisará apontar o caminho correto