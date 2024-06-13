# Usando uma imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala pipenv
RUN pip install --no-cache-dir pipenv

# Copia o Pipfile e Pipfile.lock para o diretório de trabalho
COPY Pipfile Pipfile.lock ./

# Instala as dependências do projeto
RUN pipenv install

# Copia todo o conteúdo da pasta local para o diretório de trabalho no container
COPY . .

# Exponha a porta que a aplicação vai rodar
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["pipenv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
