from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config # Import Config

# Initialize extensions outside the factory
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login' # The route name for the login page
login_manager.login_message = 'Please log in to access this page.' # Optional: customize message
login_manager.login_message_category = 'info' # Optional: category for flashed message

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models here AFTER db is initialized and associated with app
    # to avoid circular imports and ensure models are registered correctly.
    from app import models

    # Register blueprints
    from app.routes import main as main_routes
    app.register_blueprint(main_routes)

    # You might have other blueprints for errors, etc.
    # from app.errors import bp as errors_bp
    # app.register_blueprint(errors_bp)

    return app