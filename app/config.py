class Config:
    SECRET_KEY = "your_secret_key_here"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:password@db:5432/prod"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    # Add other configuration variables as needed
