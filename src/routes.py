from pprint import pprint
from .user import User as UserBackend
from flask import Flask, render_template, request, jsonify, Blueprint, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from src.message import Message
import time

# Create blueprint
main = Blueprint('main', __name__)

# Initialize the login manager (will be initialized with the app later)
login_manager = LoginManager()

# Example users database (replace with a real database in production)
USERS = {
    "user1": "password123",
    "noir@noir.noir": "noir",
    "eclipsoss": "securepassword",
    "Urpagin": "noir",
}

# User class implementing UserMixin
class User(UserMixin):
    def __init__(self, username: str):
        self.id: str = username

# In-memory messages list (replace with DB in production)
messages: list[Message] = list()
messages.append(Message(UserBackend("John"), "hello!"))
messages.append(Message(UserBackend("Urpaginator"), "It's me!"))

# Global dictionary to track active clients.
# The keys are user IDs and the values are the timestamp (in seconds) of their last activity.
active_clients = {}

# absolute genius decorator.
@main.before_request
def update_active_clients():
    """Update the active clients dictionary for each authenticated user."""
    if current_user.is_authenticated:
        # Record the current time as the last active time for the current user.
        active_clients[current_user.id] = time.time()

@main.route('/')
@login_required
def home():
    """Render main page for authenticated users."""
    return render_template("index.html")

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS:
            flash("Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
            return redirect(url_for('main.signup'))
        # Add new user (in production, store hashed passwords)
        USERS[username] = password
        flash("Inscription réussie. Veuillez vous connecter.")
        return redirect(url_for('main.login'))
    return render_template('signup.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username: str = request.form.get('username')
        password: str = request.form.get('password')
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

@main.route('/send-message', methods=['POST'])
@login_required
def send_message():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No JSON payload received")

        content: str = data.get('content')
        uuid: str = data.get('uuid')
        timestamp: int = int(data.get('timestamp'))

        # Parse the user JSON
        user_json = data.get('user')
        user = UserBackend.from_json(user_json) if user_json else None

        if content and timestamp and user and uuid:
            # Custom behavior test: clear messages if command is received.
            if content.lower() == '!clear':
                messages.clear()

            message = Message(user, content, timestamp, uuid)
            print("Message successfully appended.")
            messages.append(message)

            return jsonify({
                "status": "success",
                "message": "Message sent successfully",
                "message_id": message.uuid
            }), 201  # HTTP 201 Created

    except Exception as e:
        print(f"Error processing request: {e}")

    return jsonify({
        "status": "error",
        "message": "Invalid request. Check your request body."
    }), 400  # HTTP 400 Bad Request


@main.route('/poll')
@login_required
def poll():
    current_timestamp: float = time.time()
    last_timestamp: int = int(request.args.get('last_timestamp', 0))
    is_initial_req: int = int(request.args.get('get_history', 0))
    client_activity: dict = get_client_activity()
    print(client_activity)
    
    response: dict = {
        'messages': [],
        'client_activity': client_activity,
    }

    # If this is the initial request, return all messages.
    if is_initial_req:
        print("poll resp with hist = 1:")
        pprint([msg.to_json() for msg in messages])
        response['messages'] = [msg.to_json() for msg in messages]
        return jsonify(response)

    # Otherwise, return only messages with a timestamp greater than last_timestamp
    response['messages'] = [msg.to_json() for msg in messages if msg.timestamp > last_timestamp]
    return jsonify(response)


def get_client_activity():
    clients = get_active_clients()
    clients['inactive_users'] = list(get_inactive_clients())
    return clients

def get_active_clients():
    """
    Return the number of active clients.
    A client is considered active if their last recorded activity was within the last 30 seconds.
    """
    now = time.time()
    active_threshold = 5  # seconds
    # Filter active clients based on the threshold.
    active = {user: ts for user, ts in active_clients.items() if now - ts < active_threshold}
    count = len(active)
    return {"active_clients_count": count, "active_users": list(active.keys())}


def get_inactive_clients():
    """
    Return the number of inactive clients (registered users).
    """
    active_client_usernames = get_active_clients()['active_users']
    return {usr for usr in USERS.keys() if usr not in active_client_usernames}
    