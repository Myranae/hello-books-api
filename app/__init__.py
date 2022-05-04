from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os


db = SQLAlchemy() # SQL Alchemy object used to interact with the db
migrate = Migrate() # use when we need to change the structure of the db
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # DB Config
    if not test_config:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    
    
    db.init_app(app) # initialize SQLAlchemy object and work with the app application
    migrate.init_app(app, db) # tell migrate to work with app, and db is how to get to the db

    # Register Blueprints here
    from .routes import books_bp
    # app.register_blueprint(hello_world_bp)
    app.register_blueprint(books_bp)

    from app.models.book import Book

    return app
