import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.settings import create_app
from instance.database import db as _db  # Use the actual app's db instance
from route.index_route import index_bp
from route.ticket_route import ticket_bp


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "testsecret"

    # Register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(ticket_bp)

    # Initialize the database
    _db.init_app(app)  # Use _db here

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()  # Clean up after tests


@pytest.fixture
def client(app):
    return app.test_client()
