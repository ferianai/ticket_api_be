import models  # noqa: F401
from flask import Flask
from instance.database import init_db
from route.index_route import index_bp


def create_app(config_module="config.configure"):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configuration from a separate file
    app.config.from_object(config_module)

    # Initialize the database
    init_db(app)

    # Initialize extensions, blueprints, etc. here
    app.register_blueprint(index_bp)

    return app
