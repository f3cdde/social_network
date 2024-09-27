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

class Friendship(db.Model):
    """
    Modelo de amizade para a aplicação.

    Atributos:
        user_id (int): ID do usuário.
        friend_id (int): ID do amigo.
        timestamp (datetime): Data e hora em que a amizade foi criada.
    """
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):
    """
    Modelo de usuário para a aplicação.

    Atributos:
        id (int): ID único do usuário.
        username (str): Nome de usuário, deve ser único.
        email (str): Email do usuário, deve ser único.
        image_file (str): Nome do arquivo de imagem do perfil do usuário.
        password (str): Hash da senha do usuário.
        about_me (str): Descrição do usuário.
        last_seen (datetime): Última vez que o usuário esteve online.
        posts (list): Lista de posts associados ao usuário.
        sent_requests (list): Lista de pedidos de amizade enviados pelo usuário.
        received_requests (list): Lista de pedidos de amizade recebidos pelo usuário.
        friends (list): Lista de amigos do usuário.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    about_me = db.Column(db.Text, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)
    sent_requests = db.relationship('FriendRequest', foreign_keys='FriendRequest.sender_id', backref='sender', lazy='dynamic')
    received_requests = db.relationship('FriendRequest', foreign_keys='FriendRequest.recipient_id', backref='recipient', lazy='dynamic')
    friends = db.relationship('User', secondary='friendship', primaryjoin=(Friendship.user_id == id), secondaryjoin=(Friendship.friend_id == id), backref=db.backref('friend_of', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        """
        Representação do objeto User.

        Returns:
            str: Representação do usuário com nome de usuário, email e arquivo de imagem.
        """
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def is_friends_with(self, user):
        """
        Verifica se o usuário é amigo de outro usuário.

        Args:
            user (User): Instância do usuário a ser verificado.

        Returns:
            bool: True se os usuários são amigos, False caso contrário.
        """
        # Verifica se há uma relação de amizade entre o usuário atual e o usuário fornecido
        return self.friends.filter(Friendship.friend_id == user.id).count() > 0

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
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Coluna timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def likes_count(self):
        return Like.query.filter_by(post_id=self.id).count()

    def __repr__(self):
        """
        Representação do objeto Post.

        Returns:
            str: Representação do post com título e data de postagem.
        """
        return f"Post('{self.title}', '{self.date_posted}')"


class Message(db.Model):
    """
    Modelo de mensagem para a aplicação.

    Atributos:
        id (int): ID único da mensagem.
        sender_id (int): ID do usuário que enviou a mensagem.
        recipient_id (int): ID do usuário que recebeu a mensagem.
        body (str): Conteúdo da mensagem.
        timestamp (datetime): Data e hora em que a mensagem foi enviada.
    """
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')


    def __repr__(self):
        """
        Representação do objeto Message.

        Returns:
            str: Representação da mensagem com conteúdo e data de envio.
        """
        return f"Message('{self.body}', '{self.timestamp}')"

class FriendRequest(db.Model):
    """
    Modelo de pedido de amizade para a aplicação.

    Atributos:
        id (int): ID único do pedido de amizade.
        sender_id (int): ID do usuário que enviou o pedido de amizade.
        recipient_id (int): ID do usuário que recebeu o pedido de amizade.
        timestamp (datetime): Data e hora em que o pedido de amizade foi enviado.
        status (str): Status do pedido de amizade (pendente, aceito, rejeitado).
    """
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10), nullable=False, default='pending')

    def __repr__(self):
        """
        Representação do objeto FriendRequest.

        Returns:
            str: Representação do pedido de amizade com IDs do remetente e destinatário e status.
        """
        return f"FriendRequest('{self.sender_id}', '{self.recipient_id}', '{self.status}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')

User.likes = db.relationship('Like', back_populates='user')
Post.likes = db.relationship('Like', back_populates='post')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)

    post = db.relationship('Post', back_populates='comments')
    user = db.relationship('User')

Post.comments = db.relationship('Comment', back_populates='post')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
