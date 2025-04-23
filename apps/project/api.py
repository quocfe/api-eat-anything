from apps.helper import get_image_url
from apps.middleware import token_required
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from apps import db
from apps.project import ns
from apps.project.models import Project, serialize_project
from apps.category.models import Category
from apps.utils import res_data
from .repository import ProjectRepository

repo = ProjectRepository()

# Swagger model
project_model = ns.model(
    "Project",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(required=True, description="Project name"),
        "slug": fields.String(required=True, description="Slug"),
        "description": fields.String(description="Short description"),
        "thumbnail": fields.String(description="Thumbnail image URL"),
        "content": fields.String(description="Detailed content"),
        "link": fields.String(description="External link"),
        "year": fields.String(description="Year of the project"),
        "customer": fields.String(description="Customer name"),
        "category_id": fields.Integer(required=True, description="Category ID"),
    },
)


@ns.route("/")
class ProjectList(Resource):
    @token_required
    @ns.doc(
        params={
            "page": "Page number (default: 1)",
            "page_size": "Items per page (default: 10)",
        }
    )
    def get(self):
        try:
            page = int(request.args.get("page", 1))
            page_size = int(request.args.get("page_size", 10))
        except ValueError:
            return {"message": "Invalid pagination parameters"}, 400

        pagination = Project.query.paginate(
            page=page, per_page=page_size, error_out=False
        )
        projects = [serialize_project(p) for p in pagination.items]
        return res_data(
            projects,
            total=pagination.total,
            page=pagination.page,
            page_size=pagination.per_page,
        )


@ns.route("/get_by_category/<int:category_id>")
class ProjectListByCategory(Resource):
    @token_required
    def get(self, category_id):
        projects = repo.get_by_category(category_id)
        project_list = [serialize_project(p) for p in projects]
        return res_data(project_list, total=len(project_list), page=1, page_size=10)
