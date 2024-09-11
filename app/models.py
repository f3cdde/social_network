"""
Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
"""

from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    """
    Carrega um usuário pelo ID.

    Args:
        user_id (int): ID do usuário.

    Returns:
        User: Instância do usuário carregado.
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    Modelo de usuário para a aplicação.

    Atributos:
        id (int): ID único do usuário.
        username (str): Nome de usuário, deve ser único.
        email (str): Email do usuário, deve ser único.
        image_file (str): Nome do arquivo de imagem do perfil do usuário.
        password (str): Hash da senha do usuário.
        posts (list): Lista de posts associados ao usuário.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        """
        Representação do objeto User.

        Returns:
            str: Representação do usuário com nome de usuário, email e arquivo de imagem.
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    """
    Modelo de post para a aplicação.

    Atributos:
        id (int): ID único do post.
        title (str): Título do post.
        date_posted (datetime): Data e hora em que o post foi criado.
        content (str): Conteúdo do post.
        image_file (str): Nome do arquivo de imagem associado ao post.
        audio_file (str): Nome do arquivo de áudio associado ao post.
        video_file (str): Nome do arquivo de vídeo associado ao post.
        user_id (int): ID do usuário que criou o post.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=True)
    audio_file = db.Column(db.String(20), nullable=True)
    video_file = db.Column(db.String(20), nullable=True)  # Novo campo para vídeo
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """
        Representação do objeto Post.

        Returns:
            str: Representação do post com título e data de postagem.
        """
        return f"Post('{self.title}', '{self.date_posted}')"
