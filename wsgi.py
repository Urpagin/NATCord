#!/bin/python3

# PRODUCTION-READY

# Now, run gunicorn -w 4 wsgi:app

from src import create_app

app = create_app()
