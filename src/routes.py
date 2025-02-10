import re
import uuid
from flask import render_template, request, jsonify, Blueprint, redirect, url_for, flash
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
import time
import datetime

from src.db.schema import db, User, Message

# Create blueprint
main = Blueprint('main', __name__)

# Initialize the login manager (will be initialized with the app later)
login_manager = LoginManager()

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

        # Check if user exists in the database.
        if User.query.filter_by(username=username).first():
            flash("This username already exists. Please choose another one.")
            return redirect(url_for('main.signup'))

        # Create a new user, hash the password, and commit to DB.
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Signing up has been successful. Please sign in.")
        return redirect(url_for('main.login'))

    return render_template('signup.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username: str | None = request.form.get('username')
        password: str | None = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
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

        content = data.get('content')
        # Use provided uuid or generate a new one.
        message_uuid = data.get('uuid', str(uuid.uuid4()))

        # Custom behavior: clear messages if command received.
        # Debug feature
        if content.lower() == '!clear':
            Message.query.delete()
            db.session.commit()
            return jsonify({
                "status": "success",
                "message": "Messages cleared."
            }), 200

        # Create a new Message instance using the current user.
        new_message = Message(
            sender_id=current_user.id,
            content=content,
            uuid=message_uuid
            # The default timestamp will be set automatically.
        )
        db.session.add(new_message)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Message sent successfully",
            "message_id": new_message.uuid
        }), 201

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({
            "status": "error",
            "message": "Invalid request. Check your request body."
        }), 400


@main.route('/poll')
@login_required
def poll():
    last_timestamp = int(request.args.get('last_timestamp', 0))
    get_history = int(request.args.get('get_history', 0))

    if get_history:
        messages = Message.query.order_by(Message.timestamp).all()
    else:
        # Convert last_timestamp (Unix time) to a datetime object.
        last_dt = datetime.datetime.fromtimestamp(last_timestamp)
        messages = Message.query.filter(Message.timestamp > last_dt).order_by(Message.timestamp).all()
        
    print(f'Poll messages: {messages}. Type={messages}')
    test = [m.to_json() for m in messages]
    print(f'{test=}')
    response = {
        'messages': [msg.to_json() for msg in messages],
        'client_activity': get_client_activity()  # Retain your activity tracking if desired.
    }
    return jsonify(response)


def get_client_activity():
    now = time.time()
    active_threshold = 5  # seconds
    # Filter active clients keyed by user ID.
    active = {user_id: ts for user_id, ts in active_clients.items() if now - ts < active_threshold}
    active_ids = list(active.keys())
    
    # Query the database for users with these IDs.
    active_users = [User.query.get(user_id).username for user_id in active_ids if User.query.get(user_id)]
    
    # Get all users (by username) and determine inactive ones.
    all_users = User.query.all()
    all_usernames = {user.username for user in all_users}
    inactive_users = list(all_usernames - set(active_users))
    
    return {
        "active_clients_count": len(active_users),
        "active_users": active_users,
        "inactive_users": inactive_users
    }


@main.route('/user')
def get_user_info():
    """
    Returns information about a user.
    """
    # Get the username from the query parameters
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username not provided"}), 400

    # Retrieve the user from the database
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Return the user's information as JSON
    return jsonify(user.to_json())


@main.route('/profile', methods=['GET'])
@login_required
def profile():
    # Render the profile update page with the current user's information.
    return render_template('profile.html', user=current_user)


@main.route('/profile', methods=['POST'])
@login_required
def update_profile():
    """
    Updates the current user's profile.
    Returns a plain text error response with an appropriate HTTP status code if there is an error.
    """
    # Extract and sanitize form data.
    username = request.form.get('username', '').strip()
    old_password = request.form.get('old_password', '')
    new_password = request.form.get('new_password', '')
    chat_color = request.form.get('chat_color', '').strip()
    icon_b64 = request.form.get('icon_b64', '').strip()

    errors = []

    if not username:
        errors.append("Username cannot be empty.")
    elif username != current_user.username:
        if User.query.filter_by(username=username).first():
            errors.append("Username is already taken.")

    if chat_color:
        if not re.fullmatch(r'#[0-9a-fA-F]{6}', chat_color):
            errors.append("Invalid chat color format. Please use a hex code like #RRGGBB.")

    if new_password:
        if not old_password:
            errors.append("Old password is required to change the password.")
        elif not current_user.check_password(old_password):
            errors.append("Old password is incorrect.")
        if len(new_password) < 8:
            errors.append("New password must be at least 8 characters long.")

    # Return errors if any were encountered.
    if errors:
        return jsonify({"error": ", ".join(errors)}), 400

    # Update user fields.
    current_user.username = username
    current_user.color_hex = chat_color
    if icon_b64:
        if not icon_b64.startswith("data:image/"):
            return jsonify({"error": "Invalid icon format. Please upload a valid image."}), 400
        current_user.icon_b64 = icon_b64

    if new_password:
        current_user.set_password(new_password)

    # Attempt to commit changes.
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Return an error response with status code 500 if a database error occurs.
        return jsonify({"error": "An error occurred while updating your profile. Please try again."}), 500
    return jsonify({
        "username": current_user.username,
        "id": current_user.id,
        "color_hex": current_user.color_hex,
        "creation_time": current_user.creation_time.isoformat(),
        "icon_b64": current_user.icon_b64
    }), 200