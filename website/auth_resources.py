from flask_restx import Namespace, Resource, marshal
from .api_models import login_model, register_model, user_model
from .user_model import User
from werkzeug.security import generate_password_hash, check_password_hash
from website import db
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError


auth_ns = Namespace("auth", description="User authentication")

@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        u = User.get_by_email(auth_ns.payload["email"]) 
        if not u:
            return {"error": "User does not exist"}, 401
        if not check_password_hash(u.password_hash, auth_ns.payload["password"]):
            return {"error": "Password does not match"}, 401
        roles = u.get_roles()
        roles.append("prihlasen")
        return {"access_token":create_access_token(u.id), "roles": roles}, 200
        
@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(409, "User already exists")
    @auth_ns.response(201, "User created successfuly", user_model)
    def post(self):
        if User.get_by_email(auth_ns.payload["email"]):
            print("exists")
            return {"message": "User already exists"}, 409
        else:
            u = User()
            u.email = auth_ns.payload["email"]
            u.password_hash = generate_password_hash(auth_ns.payload["password"])
            db.session.add(u)
            db.session.commit()
            return marshal(u, user_model), 201

@auth_ns.route("/roles")
class Roles(Resource):
    def get(self):
        print("get na roles")
        verify_jwt_in_request(optional=True)
        user = User.get_by_id(get_jwt_identity())
        roles = []
        if user:
            roles = user.get_roles()
            roles.append("prihlasen")
        return {"roles": roles}, 200
        