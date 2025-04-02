import os


class Config:
    @staticmethod
    def __init_db_uri():
        # Get the base directory of this configuration file.
        base_dir: str = os.path.abspath(os.path.dirname(__file__))
        # Define the default instance directory relative to this file.
        default_db_dir: str = os.path.join("db", "instance")

        # Use environment variables if available; otherwise, use defaults.
        database_dir = os.getenv("DATABASE_DIR", os.path.join(base_dir, default_db_dir))
        database_name = os.getenv("DATABASE_NAME", "natcord.db")
        return f"sqlite:///{os.path.join(database_dir, database_name)}"

    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = __init_db_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
