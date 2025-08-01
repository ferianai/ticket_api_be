import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from models import *
from config.settings import create_app
from instance.database import db

# app = create_app("config.configure")
config_name = os.getenv("FLASK_CONFIG", "config.configure")
app = create_app(config_name)
