from flask_restx import fields
from . import api

user_model = api.model("User", {
    "id": fields.Integer,
    "email": fields.String,
    "password_hash": fields.String
})

login_model = api.model("Login", {
    "email": fields.String,
    "password": fields.String
})

register_model = api.model("Register", {
    "email": fields.String,
    "password": fields.String
})