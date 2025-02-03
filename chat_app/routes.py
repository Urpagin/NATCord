from flask import Flask, render_template, request, jsonify, Blueprint

main = Blueprint('main', __name__)
# Global list to store messages (for demonstration purposes only)
messages = []

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/channel')
def channel():
    return render_template('channel.html')

@main.route('/send', methods=['POST'])
def send_message():
    msg = request.form.get('message')
    if msg:
        messages.append(msg)
    # Return no content (HTTP 204) upon success
    return ('', 204)

@main.route('/poll')
def poll():
    # Return the full message list as JSON
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)

