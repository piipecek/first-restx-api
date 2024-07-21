from flask_restx import Namespace, Resource
from .api_models import user_model
from .user_model import User
from flask_jwt_extended import jwt_required

authorizations = {
    "jsonWebToken": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

user_ns = Namespace("user", description="Demonstration of a protected resource", authorizations=authorizations)    

@user_ns.route("/users")
class Users(Resource):
    method_decorators = [jwt_required()]
    
    @user_ns.doc(security="jsonWebToken")
    @user_ns.marshal_list_with(user_model)
    def get(self):
        return User.get_all()
        