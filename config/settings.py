from flask import Flask
from route.index_route import index_bp


def create_app(config_module="config.local"):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configuration from a separate file
    app.config.from_object(config_module)

    # Initialize extensions, blueprints, etc. here
    app.register_blueprint(index_bp)

    return app
