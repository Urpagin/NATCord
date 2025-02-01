from flask import Flask
import os
from chat_app.routes import main  # Import du Blueprint

def create_app():
    app = Flask(__name__, template_folder=os.path.abspath('templates'))

    
    from chat_app.routes import main
    app.register_blueprint(main)

    return app
