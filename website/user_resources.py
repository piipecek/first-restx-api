from flask_restx import Namespace, Resource
from .api_models import user_model
from .user_model import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from website import db

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

@user_ns.route("/<int:id>")
class UserResource(Resource):
    method_decorators = [jwt_required()]
    
    @user_ns.doc(security="jsonWebToken")
    def delete(self, id):
        identity = get_jwt_identity()
        
        #
        requesting_user = User.get_by_id(identity)
        # check, jestli smí mazat uživatele
             
        u = User.get_by_id(id)
        if u:
            db.session.delete(u)
            db.session.commit()
            return {"message": "User deleted"}, 200
        else:
            return {"message": "User not found"}, 404