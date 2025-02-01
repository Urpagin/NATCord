from flask import render_template, Blueprint

# Définition du Blueprint pour l'organisation du projet
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

