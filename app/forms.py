"""
Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from app.models import User
from markupsafe import Markup

class RegistrationForm(FlaskForm):
    """
    Formulário de registro de novos usuários.

    Campos:
        username (StringField): Nome de usuário, deve ter entre 2 e 20 caracteres.
        email (StringField): Email do usuário.
        password (PasswordField): Senha do usuário.
        confirm_password (PasswordField): Confirmação da senha, deve ser igual à senha.
        submit (SubmitField): Botão para enviar o formulário.
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        Valida se o nome de usuário já está em uso.

        Args:
            username (StringField): Nome de usuário a ser validado.

        Raises:
            ValidationError: Se o nome de usuário já estiver em uso.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """
        Valida se o email já está em uso.

        Args:
            email (StringField): Email a ser validado.

        Raises:
            ValidationError: Se o email já estiver em uso.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """
    Formulário de login de usuários.

    Campos:
        email (StringField): Email do usuário.
        password (PasswordField): Senha do usuário.
        submit (SubmitField): Botão para enviar o formulário.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    """
    Formulário para criação de novos posts.

    Campos:
        title (StringField): Título do post.
        content (TextAreaField): Conteúdo do post.
        image (FileField): Imagem do post, aceita arquivos JPG e PNG.
        audio (FileField): Áudio do post, aceita arquivos MP3 e WAV.
        video (FileField): Vídeo do post, aceita arquivos MP4 e AVI.
        submit (SubmitField): Botão para enviar o formulário.
    """
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Post Image', validators=[FileAllowed(['jpg', 'png'])])
    audio = FileField('Post Audio', validators=[FileAllowed(['mp3', 'wav'])])
    video = FileField('Post Video', validators=[FileAllowed(['mp4', 'avi'])])
    submit = SubmitField('Post')
