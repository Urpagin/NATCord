from flask import Flask
from flask_login import LoginManager
from src.db.schema import db, User  # DB models
from src.routes import main

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.Config')
    
    # Initialize the database
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id: int | str):
        return User.query.get(int(user_id))
    
    app.register_blueprint(main)
    
    with app.app_context():
        # use Flask-Migrate for prod
        db.create_all()
    
    return app
