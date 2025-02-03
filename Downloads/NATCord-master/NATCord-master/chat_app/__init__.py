from flask import Flask
from chat_app.routes import main  # Import du Blueprint

def create_app():
    app = Flask(__name__)  # Pas besoin de spécifier template_folder

    app.register_blueprint(main)

    return app
