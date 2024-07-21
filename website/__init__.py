from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from pathlib import Path

db = SQLAlchemy()
api = Api(version=1.0, title='Restx-svelte test', description="Zkušební API pro autorizaci pomocí JWT a Svelte")
jwt = JWTManager()
cors = CORS()


def create_app():
    app = Flask(__name__)
    
    db_path = Path.cwd() / "app.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(db_path)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SECRET_KEY"] = "secret"
    app.config["JWT_SECRET_KEY"] = "secrettt"
    
    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    from .user_model import User
    
    with app.app_context():
        db.create_all()

    from .auth_resources import auth_ns
    from .guest_resources import guest_ns
    from .user_resources import user_ns
    
    api.add_namespace(auth_ns)
    api.add_namespace(guest_ns)
    api.add_namespace(user_ns)

    return app