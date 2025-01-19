from flask import Flask, render_template
from flask_socketio import SocketIO

app: Flask = Flask(__name__)
app.config.from_object('config')

socketio: SocketIO = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected to websocket')

@socketio.on('message')
def handle_message(data):
    print(f'Received message: {data}')
    socketio.emit('response', f'Server received your message: {data}')


if __name__ == '__main__':
    socketio.run(app, debug=True)
