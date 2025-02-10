import os
import secrets
import logging
import colorlog
from dotenv import load_dotenv
from src import create_app
from src.db.schema import db  # Using the new schema

# Load environment variables from .env file (if it exists)
load_dotenv()

# Setup logging with color
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


# Note: basicConfig is not needed if you already configure handlers.
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def create_env(env_file, database_name, database_dir, tables_name):
    """
    Creates a .env file with the necessary environment variables if it does not exist.
    """
    if not os.path.exists(env_file):
        logging.debug(f"File {env_file} does not exist, creating it...")
        try:
            with open(env_file, "w") as file:
                # Generate and write SECRET_KEY
                key = secrets.token_hex(32)
                logging.debug("Secret key generated")
                file.write(f"SECRET_KEY={key}\n")

                # Construct and write the database URL and directory
                db_url = f"sqlite:///{database_dir}/{database_name}.db"
                file.write(f"DATABASE_URL={db_url}\n")
                logging.debug(f"Added database URL into {env_file}.")
                file.write(f"DATABASE_DIR={database_dir}\n")

                # Write table names
                for table, table_name in tables_name.items():
                    file.write(f"{table}={table_name}\n")
                    logging.debug(f"Wrote {table_name} into {env_file}.")
        except Exception as e:
            logging.error(f"An error occurred while creating {env_file}: {e}")
    else:
        logging.warning(f"File {env_file} already exists, not altering it")


def create_database(database_dir: str, database_name: str):
    """
    Creates the database (and its tables) using the Flask application factory.
    """
    # Use environment variable or fallback default for the database URL.
    database_url = os.getenv("DATABASE_URL", f"sqlite:///{database_dir}/{database_name}.db")

    # Create the database directory if it doesn't exist.
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
        logging.debug(f"Created directory: {database_dir}")

    try:
        app = create_app()
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
        with app.app_context():
            db.create_all()
        logging.debug(f"Database {database_name}.db successfully created in {database_dir}")
    except Exception as e:
        logging.error(f"Failed to create database: {e}")


if __name__ == '__main__':
    # Get the base directory of this deploy script.
    base_dir: str = os.path.abspath(os.path.dirname(__file__))
    env_file: str = os.path.join('.env')
    database_dir: str = os.path.join(base_dir, 'instance')
    database_name: str = 'natcord'

    print(os.path.join(base_dir, database_dir, database_name + '.db'))
    if os.path.exists(os.path.join(base_dir, database_dir, database_name + '.db')):
        logging.warning('Database file already exist, not re-creating it.')
        logging.warning('Deploy script halted, please delete or backup the database file to re-run this script.')
        exit(0)

    # Define table names.
    tables_name = {
        "user_table": "users",
        "message_table": "messages",
    }

    create_env(env_file, database_name, database_dir, tables_name)
    create_database(database_dir, database_name)
