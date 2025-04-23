import datetime
from apps.project import blueprint
from apps.projectItem.repository import ProjectItemRepository
from apps.utils import delete_file_if_exists, handle_file_upload, slugify
from .models import Project
from flask_login import login_required
from flask import redirect, render_template, request, url_for, flash, current_app
from apps import db
import os
from .repository import ProjectRepository
from werkzeug.utils import secure_filename


current_date = datetime.datetime.now().strftime("%Y%m%d")

from apps.category.service import (
    get_all_categories_by_type,
)


repo = ProjectRepository()
detailProject = ProjectItemRepository()


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def index():
    projects = repo.get_all()
    return render_template("project/index.html", projects=projects)


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    categories = get_all_categories_by_type("project")
    if request.method == "POST":
        dataCreate = {}
        dataCreate["name"] = request.form["name"]
        dataCreate["slug"] = slugify(request.form["name"])
        dataCreate["description"] = request.form["description"]
        thumbnail = request.files["thumbnail"]

        if thumbnail and thumbnail.filename:
            filename = handle_file_upload(thumbnail, dataCreate["slug"])
            if not filename:
                return render_template("project/create.html", categories=categories)

            dataCreate["thumbnail"] = filename

        dataCreate["category_id"] = request.form["category_id"]

        repo.create(dataCreate)
        return redirect(url_for("project_blueprint.index"))
    return render_template("project/create.html", categories=categories)


@blueprint.route("/view/<int:project_id>", methods=["GET"])
@login_required
def view(project_id):
    project = repo.get_by_id(project_id)
    mode = request.args.get("mode", "view")
    categories = get_all_categories_by_type("project")
    return render_template(
        "project/view.html", project=project, mode=mode, categories=categories
    )


@blueprint.route("/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit(project_id):
    project = repo.get_by_id(project_id)
    categories = get_all_categories_by_type("project")

    if request.method == "POST":
        dataUpdate = {}
        dataUpdate["id"] = project_id
        dataUpdate["name"] = request.form["name"]
        dataUpdate["slug"] = slugify(request.form["name"])
        dataUpdate["description"] = request.form["description"]
        thumbnail = request.files["thumbnail"]

        if thumbnail:
            new_filename = handle_file_upload(thumbnail, "project-update")
            if not new_filename:
                return render_template(
                    "project/view.html",
                    project=project,
                    mode="edit",
                    categories=categories,
                )

            if new_filename and new_filename != project.thumbnail:
                delete_file_if_exists(project.thumbnail)

            dataUpdate["thumbnail"] = new_filename

        dataUpdate["category_id"] = request.form["category_id"]
        repo.update(dataUpdate)
        return redirect(url_for("project_blueprint.index"))
    return render_template("project/index.html", project=project, categories=categories)


@blueprint.route("/<int:project_id>/delete")
@login_required
def delete(project_id):
    project = repo.get_by_id(project_id)

    if project:
        repo.delete(project.id)

        return redirect(url_for("project_blueprint.index"))
