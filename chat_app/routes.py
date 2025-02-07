from flask import Flask, render_template, request, jsonify, Blueprint, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from .message import Message
import time

# Create blueprint
main = Blueprint('main', __name__)

# Initialize the login manager (will be initialized with the app later)
login_manager = LoginManager()

# Example users database (replace with a real database in production)
USERS = {
    "user1": "password123",
    "noir@noir.noir": "noir",
    "eclipsoss": "securepassword"
}

# User class implementing UserMixin
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# # User loader callback for Flask-Login
# @login_manager.user_loader
# def load_user(user_id):
#     if user_id in USERS:
#         return User(user_id)
#     return None

# In-memory messages list (replace with DB in production)
messages: list = list()
messages.append(Message("hoi"))
messages.append(Message("hoi2"))

@main.route('/')
@login_required
def home():
    """Render main page for authenticated users."""
    return render_template("index.html")

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('main.home'))
        flash("Invalid username or password.")
        return redirect(url_for('main.login'))
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/get-private')
@login_required
def get_private():
    return "Private Info"

@main.route('/channel')
def channel():
    return render_template('channel.html')

@main.route('/send', methods=['POST'])
def send_message():
    msg = request.form.get('message')
    timestamp = request.form.get('timestamp')  # Use 'timestamp' from form data
    if msg and timestamp:
        message = Message(msg)
        message.timestamp = int(timestamp)  # Ensure integer timestamp
        messages.append(message)
    return ('', 204)  # HTTP 204: No Content

@main.route('/poll')
def poll():
    current_timestamp: float = time.time()
    last_timestamp = int(request.args.get('last_timestamp', 0))
    is_initial_req = int(request.args.get('get_history', 0))
    
    # If this is the initial request, return all messages.
    if is_initial_req:
        return jsonify([msg.content for msg in messages])
    
    # Otherwise, return only messages with a timestamp greater than last_timestamp.
    to_send = [msg.content for msg in messages if msg.timestamp > last_timestamp]
    return jsonify(to_send)

# Run the app for testing purposes.
if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'  # Required for session management
    
    # Initialize the login manager with the app
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    # Register the blueprint
    app.register_blueprint(main)
    
    app.run(debug=True)
