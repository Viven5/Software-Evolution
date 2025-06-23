from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from enhanced_blog.config import DevelopmentConfig, TestingConfig, ProductionConfig


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
bootstrap = Bootstrap()


def create_app(config_name='development'):
    app = Flask(__name__)

    if config_name == 'testing':
        app.config.from_object(TestingConfig)
    elif config_name == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

    from .auth import auth_bp
    from .posts import posts_bp
    from .main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(main_bp)

    return app
