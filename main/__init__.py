from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_assets import Environment

db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)

    db.init_app(app)

    with app.app_context():
        from . import routes, models
        # Import parts of our application
        from .auth import auth
        from .example import routes
        from .home import routes
        from .assets import compile_static_assets

        # Register Blueprints
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(example.example_bp)
        app.register_blueprint(home.home_bp)

        # Compile static assets
        compile_static_assets(assets)  # Execute logic

        db.create_all()

        return app

def init_db():
    db.drop_all()
    db.create_all()