from flask_login import UserMixin
from apps import db, login_manager
from apps.auth.util import hash_pass
from apps.base import BaseModel


class Users(BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, "__iter__") and not isinstance(value, str):
                value = value[0]
            if property == "password":
                value = hash_pass(value)
            setattr(self, property, value)

    def __repr__(self):
        return f"<User {self.username}>"


@login_manager.user_loader
def user_loader(id):
    return Users.query.get(int(id))


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    return Users.query.filter_by(username=username).first()
