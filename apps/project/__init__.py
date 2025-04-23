from flask import Blueprint
from flask_restx import Namespace

blueprint = Blueprint("project_blueprint", __name__, url_prefix="/project")
ns = Namespace("projects", description="Project Management APIs")
