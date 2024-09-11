# Social Network

Esta é uma rede social simples desenvolvida em Python, Flask e Docker. A aplicação permite registro e login de usuários, criação e exclusão de posts, e upload de imagens, vídeos e áudios.

## Estrutura do Projeto

social_network/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── post.html
│   ├── static/
│   │   ├── post_pics/
│   │   ├── post_videos/
│   │   ├── post_audios/
│   │   ├── styles.css
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md

## Dependências

- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Login
- python-dotenv

## Configuração do Ambiente

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/social_network.git

2. Navegue até o diretório do projeto:
   cd social_network

3. Crie um arquivo .env com a seguinte variável de ambiente:
   SECRET_KEY=your_secret_key

4. Construa e inicie os serviços Docker:
   docker-compose up --build

5. Acesse a aplicação no navegador em http://localhost:5000.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Passos para Garantir que o Projeto está Funcional

1. Clone o repositório: Certifique-se de que você pode clonar o repositório do GitHub.

2. Navegue até o diretório do projeto: Certifique-se de que você está no diretório onde o arquivo run.py está localizado.

3. Crie os arquivos necessários: Certifique-se de que todos os arquivos mencionados acima estão presentes e configurados corretamente.

4. Construa e inicie os serviços Docker: Construa e inicie os serviços Docker com o comando:
docker-compose up --build

5. Acesse a aplicação no navegador: Acesse a aplicação no navegador em http://localhost:5000.

## Créditos

Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
