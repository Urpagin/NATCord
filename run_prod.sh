#!/bin/bash
# run_prod.sh - Script to run the Flask app in production using Gunicorn

# Activate the virtual environment (adjust path if needed)
source venv/bin/activate

# Set environment variables for production
export FLASK_APP=wsgi.py
export FLASK_ENV=production

# Run Gunicorn with 4 worker processes
gunicorn -w 4 wsgi:app
