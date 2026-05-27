import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Створюємо об'єкт бази даних, який буде використовуватися в моделях
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Беремо URL бази даних зі змінних оточення (налаштованих у docker-compose)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'postgresql://library_user:library_password@localhost:5432/library_database'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Реєструємо маршрути (routes)
    from app.routes import bp
    app.register_blueprint(bp)

    # Створюємо таблиці в базі даних, якщо їх немає
    with app.app_context():
        db.create_all()

    return app