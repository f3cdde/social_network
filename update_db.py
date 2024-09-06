from app import app, db
from app.models import Post

with app.app_context():
    db.create_all()
