from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_session import Session

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'


def create_app():
    app = Flask(__name__)


    # Flask Configurations
    app.config['SECRET_KEY'] = 'fjalfjdas flskjfksalk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digihub.db'  # Change for PostgreSQL if needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Flask session settings
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = "filesystem"

    # Initialize session
    

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    Session(app)

    # Register Blueprint
    from app.routes import routes
    app.register_blueprint(routes)
    # app.register_blueprint(routes, url_prefix='/')

    # ✅ Wrap db.create_all() inside app.app_context()
    # with app.app_context():
    #     db.create_all()

    return app


