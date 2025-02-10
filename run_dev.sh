#!/bin/bash
# run_dev.sh - Script to run the Flask development server

# Activate the virtual environment (adjust path if needed)
source venv/bin/activate

# Set environment variables for development
export FLASK_APP=run.py
export FLASK_ENV=development

# Run the development server
flask run
