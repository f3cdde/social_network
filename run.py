from app import app, db
from flask_migrate import Migrate
from app import app, db  # Certifique-se de que você está importando seu app e banco de dados

migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
