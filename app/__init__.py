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

    app.config['SECRET_KEY'] = 'fjalfjdas flskjfksalk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///digihub.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_TYPE'] = "filesystem"

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    Session(app)

    
    from app.routes import routes
    app.register_blueprint(routes)

    return app


