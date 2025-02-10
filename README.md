# NATCord

A simple instant messenger with a UI similar to Discord.

Public instance at [https://natcord.urpagin.net](https://natcord.urpagin.net).

# Hosting

## Quick Setup (Linux)

1. **Clone the Repo:**
   ```bash
   git clone https://github.com/Urpagin/NATCord.git
   cd NATCord
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Running the App

### Development 🚀

- **Initialize the database:**
  ```
  python -m src.db.deploy
  ```

- **Manually:**
  ```bash
  export FLASK_APP=run.py
  export FLASK_ENV=development
  flask run
  ```
- **Or with Script:**
  ```bash
  ./run/run_dev.sh
  ```

### Production 🌍
- **Manually:**
  ```bash
  export FLASK_APP=wsgi.py
  export FLASK_ENV=production
  gunicorn -w 4 wsgi:app
  ```
- **Or with Script:**
  ```bash
  ./run/run_prod.sh
  ```

### Docker 🐳
- **Build & Run:**
  ```bash
  docker compose up --build
  ```
  The app will be available at [http://localhost:50742](http://localhost:50742).


## Windows & Mac
Not tested.

# Inner Workings & Technologies

We use the Python programming language and the Flask micro web framework as the backend and HTML, CSS, and JavaScript as the frontend.

The backend also has a database, which uses [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/quickstart/) (with SQLite under the hood).

For synchronization between the client and server, we originally considered using efficient methods like WebSockets or, even better, [SSE](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events) (Server-Sent Events), but we encountered difficulties implementing them. In the end, we opted for a simple yet inefficient HTTP polling system.
