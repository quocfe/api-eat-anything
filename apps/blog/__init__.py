from flask import Blueprint
from flask_restx import Namespace

blueprint = Blueprint("blog_blueprint", __name__, url_prefix="/blog")
ns = Namespace("blogs", description="Blog Management APIs")
