from flask import jsonify
from apps.home import blueprint


@blueprint.route("/api/products")
def get_products():
    products = [{"id": 1, "name": "Product A"}, {"id": 2, "name": "Product B"}]
    return jsonify(products)
