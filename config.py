import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    BASE_DIR = BASE_DIR
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, os.getenv("DATABASE_DIR", "instance"), os.getenv("DATABASE_NAME", "natcord.db"))}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
