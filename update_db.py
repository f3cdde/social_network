"""
Desenvolvido por (Developed by / 開發者) Felipe Ferreira (f3cdde)
"""

from app import app, db
from app.models import Post

with app.app_context():
    db.create_all()
