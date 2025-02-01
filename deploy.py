import os
import secrets
import logging
import colorlog
from chat_app import create_app
from chat_app.models import db




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




def create_env(env_file, database_name, database_dir):
    if not os.path.exists(env_file):    
        logging.info(f'File {env_file} does not exist, creating it...')
        with open(env_file, "w") as file:
            try:
                key = secrets.token_hex(32)
                logging.info("Secret key generated")
                file.write(f"SECRET_KEY={key}")
            except Error:
                logging.error(f"An error occured: {Error}")


            try:
                db_name = f"database={database_name}.db"       
                file.write(db_name)
                logging.info(f"Adding databse name into {env_file} file.")
                file.write(f"database_dir={database_dir}")
            except Error:
                logging.error(f"Failed to write into file {env_file} file: {Error}")
    else:
        logging.warning(f"File {env_file} already exist, not altering it")



def create_database(database_dir,database_name):
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
        try:
            app = create_app()
            with app.app_context():
                db.create_all()
            logging.info(f"Create {database_name} into {database_dir}")
        except E:
            logging.info(f"Failed to create database: {e}")





if __name__ == "__main__":
    env_file = '.env'
    database_dir = "instance"
    database_name = "natcord"
    # Tables
    user_table = "User"
    friendship_table = "Friendship"
    serber_table = "Server"
    channel_table = "Channel"
    conversation_table = "Conversation"
    conversation_participant_table = "Conversation_participant"
    message_table = "Message"
    file_table = "File"

    
    create_database(database_dir, database_name)
    create_env(env_file, database_name)