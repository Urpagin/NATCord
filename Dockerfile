FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Expose the port (Gunicorn listens on 8000 inside the container)
EXPOSE 8000

# Use the wsgi.py entry point
CMD ["gunicorn", "-w", "4", "wsgi:app", "-b", "0.0.0.0:8000"]

