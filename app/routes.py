"""
Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
"""

import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, PostForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image


def save_file(form_file, folder):
    """
    Salva um arquivo enviado pelo usuário em um diretório específico.

    Args:
        form_file (FileStorage): Arquivo enviado pelo usuário.
        folder (str): Diretório onde o arquivo será salvo.

    Returns:
        str: Nome do arquivo salvo.
    """
    # Gera um nome de arquivo único usando um hash hexadecimal
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(app.root_path, 'static', folder, file_fn)

    # Salva o arquivo no diretório especificado
    form_file.save(file_path)
    return file_fn


@app.route("/")
@app.route("/home")
@login_required
def home():
    """
    Rota para a página inicial, exibindo os posts do usuário logado.

    Returns:
        str: Renderização do template 'home.html' com os posts do usuário.
    """
    posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Rota para a página de registro de novos usuários.

    Returns:
        str: Renderização do template 'register.html' com o formulário de registro.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Cria um hash da senha para armazenamento seguro
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        # Adiciona o novo usuário ao banco de dados
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Rota para a página de login de usuários.

    Returns:
        str: Renderização do template 'login.html' com o formulário de login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    """
    Rota para logout do usuário.

    Returns:
        str: Redirecionamento para a página inicial.
    """
    logout_user()
    return redirect(url_for('home'))


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
    Rota para criação de um novo post.

    Returns:
        str: Renderização do template 'post.html' com o formulário de novo post.
    """
    form = PostForm()
    if form.validate_on_submit():
        # Salva os arquivos de imagem, áudio e vídeo, se fornecidos
        image_file = save_file(form.image.data, 'post_pics') if form.image.data else None
        audio_file = save_file(form.audio.data, 'post_audios') if form.audio.data else None
        video_file = save_file(form.video.data, 'post_videos') if form.video.data else None

        # Cria um novo post com os dados fornecidos
        post = Post(title=form.title.data, content=form.content.data, image_file=image_file, audio_file=audio_file,
                    video_file=video_file, author=current_user)

        # Adiciona o novo post ao banco de dados
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('post.html', title='New Post', form=form)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Rota para deletar um post.

    Args:
        post_id (int): ID do post a ser deletado.

    Returns:
        str: Redirecionamento para a página inicial.
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    # Remove o post do banco de dados
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))
