from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# Uncomment for DB
#from .db.schema import User
from src.db.schema import db
from src.routes import User

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.Config')

    # Initialisation de la base de données
    db.init_app(app)

    # Initialisation de Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    # TODO: UNCOMMENT FOR DB USE
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    @login_manager.user_loader
    def load_user(user_id):
        from .routes import USERS
        if user_id in USERS:
            return User(user_id)
        return None

    from src.routes import main
    app.register_blueprint(main)

    return app

