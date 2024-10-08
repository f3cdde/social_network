"""
Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
"""

import hmac
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

class Bcrypt:
    """
    Classe para integração do Bcrypt com Flask.

    Métodos:
        __init__(app=None): Inicializa a classe Bcrypt.
        init_app(app): Configura a aplicação Flask para usar Bcrypt.
        generate_password_hash(password, rounds=None): Gera um hash para a senha fornecida.
        check_password_hash(pw_hash, password): Verifica se a senha fornecida corresponde ao hash armazenado.
    """

    def __init__(self, app=None):
        """
        Inicializa a classe Bcrypt.

        Args:
            app (Flask): Instância da aplicação Flask (opcional).
        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Configura a aplicação Flask para usar Bcrypt.

        Args:
            app (Flask): Instância da aplicação Flask.
        """
        app.extensions['bcrypt'] = self

    def check_password_hash(self, pw_hash, password):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.

        Args:
            pw_hash (str): Hash armazenado da senha.
            password (str): Senha fornecida para verificação.

        Returns:
            bool: True se a senha corresponder ao hash, False caso contrário.
        """
        return check_password_hash(pw_hash, password)


    def check_password_hash(self, pw_hash, password):
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.

        Args:
            pw_hash (str): Hash armazenado da senha.
            password (str): Senha fornecida para verificação.

        Returns:
            bool: True se a senha corresponder ao hash, False caso contrário.
        """
        return hmac.compare_digest(pw_hash, generate_password_hash(password))
