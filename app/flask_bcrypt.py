import hmac
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

class Bcrypt:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.extensions['bcrypt'] = self

    def generate_password_hash(self, password, rounds=None):
        if rounds is None:
            rounds = current_app.config.get('BCRYPT_LOG_ROUNDS', 12)
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_password_hash(self, pw_hash, password):
        return hmac.compare_digest(pw_hash, generate_password_hash(password))
