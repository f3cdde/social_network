"""
Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
"""

import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, PostForm, MessageForm, ProfileForm, FriendRequestForm
from app.models import User, Post, Message, FriendRequest, Friendship, Comment, Notification, Like
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
    Rota para a página inicial, exibindo os posts do usuário logado e dos amigos.

    Returns:
        str: Renderização do template 'home.html' com os posts do usuário e amigos.
    """
    # Busca os posts dos amigos, excluindo o usuário atual
    friends_posts = Post.query.filter(
        Post.author.has(Friendship.friend_id == current_user.id),
        Post.user_id != current_user.id  # Exclui os posts do próprio usuário
    ).order_by(Post.timestamp.desc()).all()

    # Busca os posts do usuário logado
    user_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.timestamp.desc()).all()
    
    # Combina os posts do usuário e dos amigos
    posts = user_posts + friends_posts

    # Ordena os posts por timestamp decrescente (do mais recente ao mais antigo)
    posts.sort(key=lambda post: post.timestamp, reverse=True)

    # Contagem de notificações
    notification_count = Notification.query.filter_by(user_id=current_user.id).count()

    # Renderiza o template passando os posts e a contagem de notificações
    return render_template('home.html', posts=posts, notification_count=notification_count)

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

    # Remove os likes associados ao post
    Like.query.filter_by(post_id=post_id).delete()  # Remove todos os likes desse post

    # Remove o post do banco de dados
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    """
    Redireciona para a página de mensagens com o destinatário selecionado.
    """
    user = User.query.filter_by(username=recipient).first_or_404()
    if not current_user.is_friends_with(user):
        flash('You can only send messages to your friends.', 'danger')
        return redirect(url_for('messages'))

    # Redireciona para a página de mensagens com o destinatário pré-selecionado
    return redirect(url_for('messages', selected_recipient=recipient))


@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    """
    Rota para visualizar mensagens enviadas e recebidas, e exibir amigos para iniciar novas conversas.
    """
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    received_messages = Message.query.filter_by(recipient_id=current_user.id).all()
    friends = current_user.friends.all()

    # Para pré-selecionar o destinatário ao redirecionar de send_message/<recipient>
    selected_recipient = request.args.get('selected_recipient', None)

    if request.method == 'POST':
        recipient_username = request.form.get('recipient')
        message_body = request.form.get('body')

        recipient = User.query.filter_by(username=recipient_username).first()

        if recipient and current_user.is_friends_with(recipient):
            # Criar a mensagem
            new_message = Message(sender_id=current_user.id, recipient_id=recipient.id, body=message_body)
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent successfully!', 'success')
        else:
            flash('Failed to send the message. Invalid recipient.', 'danger')

        return redirect(url_for('messages'))

    return render_template(
        'messages.html',
        sent_messages=sent_messages,
        received_messages=received_messages,
        friends=friends,
        selected_recipient=selected_recipient
    )

@app.route('/user/<username>')
@login_required
def user_profile(username):
    """
    Rota para visualizar o perfil de um usuário.

    Args:
        username (str): Nome de usuário.

    Returns:
        str: Renderização do template 'user_profile.html' com as informações do usuário.
    """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    Rota para editar o perfil do usuário.

    Returns:
        str: Renderização do template 'edit_profile.html' com o formulário de edição de perfil.
    """
    form = ProfileForm()
    if form.validate_on_submit():
        # Atualiza os dados do perfil do usuário
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user_profile', username=current_user.username))
    elif request.method == 'GET':
        # Preenche o formulário com os dados atuais do usuário
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/send_friend_request', methods=['GET', 'POST'])
@login_required
def send_friend_request():
    """
    Rota para enviar um pedido de amizade.

    Returns:
        str: Renderização do template 'send_friend_request.html' com o formulário de pedido de amizade.
    """
    form = FriendRequestForm()
    if form.validate_on_submit():
        # Busca o destinatário pelo nome de usuário
        recipient = User.query.filter_by(username=form.username.data).first()
        if recipient:
            if recipient.id == current_user.id:  # Adiciona a validação aqui
                flash('You cannot send a friend request to yourself.', 'danger')
                return redirect(url_for('home'))
            # Cria um novo pedido de amizade
            friend_request = FriendRequest(sender_id=current_user.id, recipient_id=recipient.id)
            db.session.add(friend_request)
            db.session.commit()
            flash('Friend request sent!', 'success')
        else:
            flash('User not found.', 'danger')
        return redirect(url_for('home'))
    return render_template('send_friend_request.html', title='Send Friend Request', form=form)

@app.route('/friend_requests')
@login_required
def friend_requests():
    """
    Rota para visualizar pedidos de amizade recebidos.

    Returns:
        str: Renderização do template 'friend_requests.html' com os pedidos de amizade recebidos.
    """
    # Busca todos os pedidos de amizade pendentes recebidos pelo usuário atual
    requests = FriendRequest.query.filter_by(recipient_id=current_user.id, status='pending').all()
    return render_template('friend_requests.html', requests=requests)

@app.route('/accept_friend_request/<int:request_id>')
@login_required
def accept_friend_request(request_id):
    """
    Rota para aceitar um pedido de amizade.

    Args:
        request_id (int): ID do pedido de amizade.

    Returns:
        str: Redirecionamento para a página de pedidos de amizade.
    """
    # Busca o pedido de amizade pelo ID
    friend_request = FriendRequest.query.get_or_404(request_id)
    if friend_request.recipient_id != current_user.id:
        abort(403)
    # Atualiza o status do pedido de amizade para 'accepted'
    friend_request.status = 'accepted'
    # Cria relações de amizade bidirecionais
    friendship1 = Friendship(user_id=current_user.id, friend_id=friend_request.sender_id)
    friendship2 = Friendship(user_id=friend_request.sender_id, friend_id=current_user.id)
    db.session.add(friend_request)
    db.session.add(friendship1)
    db.session.add(friendship2)
    db.session.commit()
    flash('Friend request accepted!', 'success')
    return redirect(url_for('friend_requests'))

@app.route('/reject_friend_request/<int:request_id>')
@login_required
def reject_friend_request(request_id):
    """
    Rota para rejeitar um pedido de amizade.

    Args:
        request_id (int): ID do pedido de amizade.

    Returns:
        str: Redirecionamento para a página de pedidos de amizade.
    """
    # Busca o pedido de amizade pelo ID
    friend_request = FriendRequest.query.get_or_404(request_id)
    if friend_request.recipient_id != current_user.id:
        abort(403)
    # Atualiza o status do pedido de amizade para 'rejected'
    friend_request.status = 'rejected'
    db.session.add(friend_request)
    db.session.commit()
    flash('Friend request rejected.', 'success')
    return redirect(url_for('friend_requests'))

@app.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Verifica se o usuário já curtiu o post
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    
    if like is None:
        # Adiciona o like se o usuário não tiver curtido
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        liked = True
    else:
        # Remove o like se o usuário já tiver curtido
        db.session.delete(like)
        db.session.commit()
        liked = False

    # Retorna JSON com o estado do like e a contagem atualizada
    likes_count = Like.query.filter_by(post_id=post_id).count()  # Contagem de likes
    return jsonify({'liked': liked, 'likes_count': likes_count})


@app.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    comment_body = request.form.get('body')
    comment = Comment(body=comment_body, post_id=post.id, user_id=current_user.id)
    db.session.add(comment)
    db.session.commit()
    flash('Comment added!', 'success')
    return redirect(url_for('home'))  # ou para a página do post

@app.route('/friends')
@login_required
def friends():
    friends = current_user.friends  # Certifique-se de que isso retorne uma lista de amigos
    if not friends:  # Adicione verificação para amigos vazios
        flash('You have no friends yet.')  # Use um flash para informar o usuário
    return render_template('friends.html', friends=friends)

@app.route('/notifications')
@login_required
def notifications():
    # Aqui você irá buscar as notificações do usuário
    notifications_list = Notification.query.filter_by(user_id=current_user.id).all()  # Ajuste conforme seu modelo
    return render_template('notifications.html', notifications=notifications_list)

@app.context_processor
def inject_notification_count():
    if current_user.is_authenticated:
        notification_count = Notification.query.filter_by(user_id=current_user.id).count()
        return dict(notification_count=notification_count)
    return dict(notification_count=0)
