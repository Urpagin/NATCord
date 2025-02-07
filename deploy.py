import os
import secrets
import logging
import colorlog
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from src import create_app
from src.models import db

load_dotenv()

handler = logging.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def create_env(env_file, database_name, database_dir, tables_name):
    if not os.path.exists(env_file):    
        logging.debug(f'File {env_file} does not exist, creating it...')
        with open(env_file, "w") as file:
            try:
                key = secrets.token_hex(32)
                logging.debug("Secret key generated")
                file.write(f"SECRET_KEY={key}\n")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                db_url = f"sqlite:///{database_dir}/{database_name}.db"       
                file.write(f"DATABASE_URL={db_url}\n")
                logging.debug(f"Adding database URL into {env_file} file.")
                file.write(f"DATABASE_DIR={database_dir}\n")
            except Exception as e:
                logging.error(f"Failed to write into file {env_file}: {e}")

            for table, table_name in tables_name.items():
                try:
                    file.write(f"{table}={table_name}\n")
                    logging.debug(f"Wrote {table_name} into {env_file}.")
                except Exception as e:
                    logging.error(f"Failed to write into {env_file}: {e}")
    else:
        logging.warning(f"File {env_file} already exists, not altering it")

def create_database():
    database_dir = os.getenv("DATABASE_DIR", "instance")
    database_name = os.getenv("DATABASE_NAME", "natcord")
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{database_dir}/{database_name}.db")
    
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
        logging.debug(f"Created directory: {database_dir}")
    
    try:
        app = create_app()
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        with app.app_context():
            db.create_all()
        logging.debug(f"Database {database_name}.db successfully created in {database_dir}")
    except Exception as e:
        logging.error(f"Failed to create database: {e}")

if __name__ == "__main__":
    env_file = '.env'
    database_dir = "instance"
    database_name = "natcord"
    
    # Tables
    tables_name = {
        "user_table": "User",
        "friendship_table": "Friend",
        "server_table": "Server",
        "channel_table": "Channel",
        "conversation_participant_table": "Conversation_participant",
        "conversation_table": "Conversation",
        "message_table": "Message",
        "file_table": "File",
    }
    
    create_env(env_file, database_name, database_dir, tables_name)
    create_database()
