"""
This module handles the creation of the application's instance
Various extensions are initialized and configuration settings are also attached
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate


# Create instances from the installed extensions
db = SQLAlchemy()
migrate = Migrate(db, render_as_batch=True)
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page'
# Categorize the login required message
login.login_message_category = 'info'


def create_app(config_class=Config):
    """
    Factory function that creates an instance of a flask application
    and attaches the various configurations to the application
    """
    app = Flask(__name__)
    # attach the configuration variables from the application
    app.config.from_object(Config)

    # initialize objects derived from the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # register blueprints to the application
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.books import bp as books_bp
    app.register_blueprint(books_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
