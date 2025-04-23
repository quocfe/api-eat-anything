from apps.category import blueprint
from apps.category.repository import CategoryRepository
from apps.utils import slugify
from .models import Category
from flask_login import login_required
from flask import redirect, render_template, request, url_for
from apps import db
from .service import (
    get_all_categories,
    create_category,
    update_category,
    delete_category,
)

repo = CategoryRepository()


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        name = request.form["name"]
        type_ = request.form["type"]
        cat_id = request.form.get("id")

        if cat_id:
            # Update category
            data_update = {
                "name": name,
                "type": type_,
                "cat_id": cat_id,
            }
            print("update")
            repo.update(data_update)
        else:
            # Create category
            print("create")
            data_update = {
                "name": name,
                "slug": slugify(name),
                "type": type_,
            }
            repo.create(data_update)
            # create_category(name, type_)

        return redirect(url_for("category_blueprint.index"))

    categories = repo.get_all()
    return render_template("category/index.html", categories=categories)


@blueprint.route("/delete/<int:id>", methods=["POST"])
def delete_category_route(id):
    repo.delete(id)
    return redirect(url_for("category_blueprint.index"))  # Redirect về index
