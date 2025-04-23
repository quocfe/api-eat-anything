from flask import Blueprint
from flask_restx import Namespace

blueprint = Blueprint("projectItem_blueprint", __name__, url_prefix="/projectItem")
ns = Namespace("projects", description="Project Management APIs")
