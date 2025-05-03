from flask import Blueprint

# Create a blueprint for the routes
main = Blueprint('main', __name__)

from . import pages, errors  # Import the routes for pages and errors to register them with the blueprint
# TODO: Define or import actual routes here