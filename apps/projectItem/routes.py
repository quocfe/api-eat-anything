import datetime
import os
from apps.project.models import Project
from apps.project.repository import ProjectRepository
from apps.projectItem import blueprint
from apps.projectItem.repository import ProjectItemRepository
from apps.utils import handle_file_upload
from .models import ProjectItem
from flask import render_template, current_app, request, redirect, url_for, flash
from werkzeug.utils import secure_filename


current_date = datetime.datetime.now().strftime("%Y%m%d")


repo = ProjectItemRepository()
projectRepo = ProjectRepository()


@blueprint.route("/<project_id>")
def list_items(project_id):
    project = Project.query.get_or_404(project_id)
    project_items = ProjectItem.query.filter_by(project_id=project_id).all()
    return render_template(
        "project/list_items.html", project=project, project_items=project_items
    )


@blueprint.route("/<int:project_id>/add-items", methods=["GET", "POST"])
def add_items(project_id):
    project = Project.query.get_or_404(project_id)
    project_items = ProjectItem.query.filter_by(project_id=project_id).all()
    if request.method == "POST":
        items = []
        for key in request.files:
            if "image" in key:
                index = key.split("[")[1].split("]")[0]
                image = request.files[key]
                description = request.form.get(f"items[{index}][description]")
                items.append({"image": image, "description": description})

        for item in items:
            filename = handle_file_upload(item["image"], "project-item")
            if not filename:
                return redirect(request.url)

            data = {
                "project_id": project.id,
                "image": filename,
                "description": item["description"],
            }

            repo.create(data)
        return redirect(
            url_for("projectItem_blueprint.list_items", project_id=project.id)
        )

    return render_template(
        "project/add_items.html", project=project, project_items=project_items
    )


@blueprint.route("/<int:project_id>/deleteItem/<int:item_id>", methods=["POST"])
def delete_item(project_id, item_id):
    item = ProjectItem.query.filter_by(id=item_id, project_id=project_id).first_or_404()

    if item:
        repo.delete(item.id)

    return redirect(url_for("projectItem_blueprint.list_items", project_id=project_id))


@blueprint.route("/<int:item_id>/edit", methods=["GET", "POST"])
def update_item(item_id):
    item = repo.get_by_id(item_id)
    project = projectRepo.get_by_id(item.project_id)

    if request.method == "POST":
        item.description = request.form["description"]
        # Check if a new image is uploaded
        if "image" in request.files and request.files["image"].filename != "":
            image = request.files["image"]
            ext = os.path.splitext(image.filename)[1]
            filename = f"{'project-item-update'}-{current_date}{ext}"
            image_filename = secure_filename(filename)
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            new_image_path = os.path.join(upload_folder, image_filename)

            old_image_path = os.path.join(upload_folder, item.image)
            if os.path.exists(old_image_path) and item.image != filename:
                try:
                    os.remove(old_image_path)
                except Exception as e:
                    print(f"Do not delete the old image: {e}")

            # Lưu ảnh mới
            image.save(new_image_path)
            item.image = filename

        repo.update(item)
        return redirect(
            url_for("projectItem_blueprint.list_items", project_id=project.id)
        )

    return render_template("project/edit_item.html", project=project, item=item)
