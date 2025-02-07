# NATCord

A simple instant messenger with a UI similar to Discord.

# Hosting

## Linux
For now:

`git clone --branch dev --single-branch https://github.com/Urpagin/NATCord.git`

`cd NATCord`

`python -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

`python run.py`

## Windows & Mac
Not tested.

# Inner Workings & Technologies

We use the Python programming language and the Flask micro web framework as the backend and HTML, CSS, and JavaScript as the frontend.

The backend also has a database, which uses [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/) (with SQLite under the hood).

For synchronization between the client and server, we originally considered using efficient methods like WebSockets or, even better, [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) (Server-Sent Events), but we encountered difficulties implementing them. In the end, we opted for a simple yet inefficient HTTP polling system.
