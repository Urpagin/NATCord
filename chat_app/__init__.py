from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from chat_app.models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialisation de la base de données
    db.init_app(app)

    # Initialisation de Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from chat_app.routes import main
    app.register_blueprint(main)

    return app

