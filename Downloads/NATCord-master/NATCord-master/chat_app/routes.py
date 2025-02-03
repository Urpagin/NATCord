from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    print("Chargement de index.html...")  # Debugging
    return render_template('index.html')

@main.route('/login')
def login():
    print("Chargement de login.html...")  # Debugging
    return render_template('login.html')

@main.route('/register')
def register():
    print("Chargement de register.html...")  # Debugging
    return render_template('register.html')
