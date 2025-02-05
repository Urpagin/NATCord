from flask import Flask, render_template, request, jsonify, Blueprint, redirect, url_for, session
from .message import Message
import time

main = Blueprint('main', __name__)

# replace with DB
messages: Message = list()

messages.append(Message("hoi"))
messages.append(Message("hoi2"))

# Example users database
# replace with DB
USERS = {
    "user1": "password123",
    "eclipsoss": "securepassword"
}

# todo: auth,
# - js side: put password and usernamd in JSON body
#   and check with all requests client-side and server-side.
#
# - salt passwords in db.

@main.route('/')
def home():
    """Redirect to login if not authenticated"""
    return render_template("index.html")  # Show main page if logged in

    if "username" not in session:
        return redirect(url_for("main.login"))
    return render_template("index.html")  # Show main page if logged in

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/channel')
def channel():
    return render_template('channel.html')

@main.route('/send', methods=['POST'])
def send_message():
    msg = request.form.get('message')
    timestamp = request.form.get('timestamp')  # Fix: Use 'timestamp' instead of 'message'

    if msg and timestamp:
        message = Message(msg)
        message.timestamp = int(timestamp)  # Ensure it's stored as an integer
        messages.append(message)
        
    return ('', 204)  # HTTP 204: No Content


@main.route('/poll')
def poll():
    current_timestamp: float = time.time()

    last_timestamp = int(request.args.get('last_timestamp', 0))  # Get timestamp from URL
    is_initial_req = int(request.args.get('get_history', 0))  # Get timestamp from URL

    # Return all of the messages (to initialize the history on the client side)
    if is_initial_req:
        return jsonify([msg.content for msg in messages])

    # Only keep messages the client has not 
    to_send = [msg.content for msg in messages if msg.timestamp > last_timestamp]


    # Return the full message list as JSON
    return jsonify(to_send)

if __name__ == '__main__':
    app.run(debug=True)

