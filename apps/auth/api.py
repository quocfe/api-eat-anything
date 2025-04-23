# apps/auth/api.py

from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_user, current_user, login_required
from apps.auth.models import Users, db
from apps.auth.util import hash_pass, verify_pass

ns = Namespace("auth", description="Authentication APIs")

# Swagger models
register_model = ns.model(
    "Register",
    {
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

login_model = ns.model(
    "Login",
    {
        "username": fields.String(required=True),
        "password": fields.String(required=True),
    },
)


# Register API
@ns.route("/register")
class Register(Resource):
    @ns.expect(register_model)
    def post(self):
        data = request.json
        if Users.query.filter_by(username=data["username"]).first():
            return {"message": "Username already exists"}, 400
        if Users.query.filter_by(email=data["email"]).first():
            return {"message": "Email already registered"}, 400

        new_user = Users(
            username=data["username"],
            email=data["email"],
            password=data["password"],  # auto hash trong constructor
        )
        db.session.add(new_user)
        db.session.commit()

        return {"message": "Registration successful"}, 201


# Login API
@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model)
    def post(self):
        data = request.json
        user = Users.query.filter_by(username=data["username"]).first()
        if not user or not verify_pass(data["password"], user.password):
            return {"message": "Invalid credentials"}, 401

        login_user(user)
        return {"message": "Login successful"}, 200


# Profile API
