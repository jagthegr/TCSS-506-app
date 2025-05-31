import os
from pathlib import Path
from dotenv import load_dotenv

current_path = Path(__file__)
base_dir = current_path.parent.parent.absolute()
env_path = (base_dir / ".env").absolute()
load_dotenv(env_path)


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or (
        f"sqlite:///{base_dir/'instance'/ 'site.db'}"
    )
    DEBUG = True
    # Add other configuration variables as needed
