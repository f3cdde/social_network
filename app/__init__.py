"""
Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from .context_processors import inject_notifications


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa a aplicação Flask
app = Flask(__name__)

#Injetor de notificações
@app.context_processor
def notifications():
    return inject_notifications()

# Configurações da aplicação
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Chave secreta para segurança da aplicação
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # URI do banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilita rastreamento de modificações do SQLAlchemy

# Inicializa as extensões
db = SQLAlchemy(app)  # Banco de dados SQLAlchemy
migrate = Migrate(app, db)  # Migrações do banco de dados
bcrypt = Bcrypt(app)  # Hashing de senhas com Bcrypt
login_manager = LoginManager(app)  # Gerenciamento de login
login_manager.login_view = 'login'  # Rota para a página de login

# Importa os módulos de rotas e modelos
from app import routes, models
