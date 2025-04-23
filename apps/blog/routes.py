import datetime
import os
from flask import (
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from apps.blog import blueprint
from apps.utils import delete_file_if_exists, handle_file_upload, slugify
from .models import Blog
from .repository import BlogRepository
from apps.category.repository import CategoryRepository
from apps import db

current_date = datetime.datetime.now().strftime("%Y%m%d")

repo = BlogRepository()
cateRepo = CategoryRepository()


@blueprint.route("/", methods=["GET"])
# @login_required
def index():
    page = request.args.get("page", 1, type=int)
    pagination = repo.get_paginated(page=page, per_page=5)
    blogs = pagination.items
    return render_template("blog/index.html", blogs=blogs, pagination=pagination)


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    categories = cateRepo.get_all_categories_by_type("blog")
    if request.method == "POST":
        dataCreate = {
            "title": request.form["title"],
            "slug": slugify(request.form["title"]),
            "description": request.form["description"],
            "content": request.form["content"],
            "author_id": current_user.id,
            "category_id": request.form["category_id"],
        }

        thumbnail = request.files["thumbnail"]
        if thumbnail and thumbnail.filename:
            filename = handle_file_upload(thumbnail, dataCreate["slug"])
            if not filename:
                return render_template("blog/create.html", categories=categories)

            dataCreate["thumbnail"] = filename

        repo.create(dataCreate)

        return redirect(url_for("blog_blueprint.index"))

    return render_template("blog/create.html", categories=categories)


@blueprint.route("/view/<int:blog_id>", methods=["GET"])
@login_required
def view(blog_id):
    blog = repo.get_by_id(blog_id)
    mode = request.args.get("mode", "view")
    categories = cateRepo.get_all_categories_by_type("blog")
    return render_template(
        "blog/view.html", blog=blog, mode=mode, categories=categories
    )


@blueprint.route("/<int:blog_id>/edit", methods=["GET", "POST"])
@login_required
def edit(blog_id):
    blog = repo.get_by_id(blog_id)
    categories = cateRepo.get_all_categories_by_type("blog")

    if request.method == "POST":
        dataUpdate = {
            "id": blog_id,
            "title": request.form["title"],
            "slug": slugify(request.form["title"]),
            "description": request.form["description"],
            "content": request.form["content"],
            "category_id": request.form["category_id"],
        }

        thumbnail = request.files["thumbnail"]
        if thumbnail:
            new_filename = handle_file_upload(thumbnail, "blog-update")
            if not new_filename:
                return render_template(
                    "blog/view.html", blog=blog, mode="edit", categories=categories
                )
            if new_filename and new_filename != blog.thumbnail:
                delete_file_if_exists(blog.thumbnail)

            dataUpdate["thumbnail"] = new_filename

        repo.update(dataUpdate)
        return redirect(url_for("blog_blueprint.index"))

    return render_template("blog/edit.html", blog=blog, categories=categories)


@blueprint.route("/<int:blog_id>/delete")
@login_required
def delete(blog_id):
    blog = repo.get_by_id(blog_id)
    if blog:
        repo.delete(blog.id)
    return redirect(url_for("blog_blueprint.index"))
