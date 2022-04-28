from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development

db = SQLAlchemy() # SQL Alchemy object used to interact with the db
migrate = Migrate() # use when we need to change the structure of the db

def create_app(test_config=None):
    app = Flask(__name__)

    # DB Config
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development"
    
    
    db.init_app(app) # initialize SQLAlchemy object and work with the app application
    migrate.init_app(app, db) # tell migrate to work with app, and db is how to get to the db

    # Register Blueprints here
    from .routes import books_bp
    # app.register_blueprint(hello_world_bp)
    app.register_blueprint(books_bp)

    from app.models.book import Book

    return app
