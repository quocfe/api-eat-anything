from flask import Blueprint
from flask_restx import Namespace

blueprint = Blueprint("category_blueprint", __name__, url_prefix="/category")
ns = Namespace("categories", description="Category Management APIs")
