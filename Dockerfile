# Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)

# Use uma imagem base oficial do Python
FROM python:3.8-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt ./

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do projeto para o diretório de trabalho
COPY . .
#COPY ./app/site.db /app/site.db

# Exponha a porta 5000
EXPOSE 5000

# Comando para iniciar o servidor
 CMD ["python", "run.py"]

