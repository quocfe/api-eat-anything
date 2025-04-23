from apps.middleware import token_required
from flask import request
from flask_restx import Resource, fields
from apps.blog.models import Blog
from apps.blog import ns
from apps.utils import res_data


# Swagger models
blog_model = ns.model(
    "Blog",
    {
        "id": fields.Integer(readonly=True),
        "title": fields.String(required=True, description="Blog title"),
        "slug": fields.String(required=True, description="Blog slug"),
        "content": fields.String(required=True, description="Blog content"),
        "category_id": fields.Integer(required=True, description="Category ID"),
    },
)


# Get all blogs API
@ns.route("/")
class BlogList(Resource):
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

        pagination = Blog.query.paginate(page=page, per_page=page_size, error_out=False)
        blogs = [p.serialize() for p in pagination.items]
        return res_data(
            blogs,
            total=pagination.total,
            page=pagination.page,
            page_size=pagination.per_page,
        )
