from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_session import Session
from config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'


def create_app():
    app = Flask(__name__)

    # Load configuration from Config class
    app.config.from_object(Config)

    # Upload config
    import os
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'mp4', 'mov', 'doc', 'docx'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

    # Session config
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = "filesystem"

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    Session(app)

    print("Using database:", app.config['SQLALCHEMY_DATABASE_URI'])

    from app.routes import routes
    app.register_blueprint(routes)

    return app
