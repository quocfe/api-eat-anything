from apps.category.service import get_all_categories_by_type
from apps.middleware import token_required
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from apps.category.models import Category, db
from apps.utils import slugify

ns = Namespace("categories", description="Category Management APIs")

CATEGORY_TYPES = ["blog", "product"]

category_model = ns.model(
    "Category",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String(required=True, description="Category name"),
        "type": fields.String(
            required=True, description="Category type", enum=CATEGORY_TYPES
        ),
    },
)


@ns.route("/by-type/<string:type>")
@ns.param("type", "Category type", enum=CATEGORY_TYPES)
class CategoryByType(Resource):
    @token_required
    def get(self, type):
        categories = get_all_categories_by_type(type)
        if not categories:
            return {"message": f"No categories found for type '{type}'"}, 404

        cate_list = [
            {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "type": category.type,
            }
            for category in categories
        ]

        return jsonify(cate_list)
