from flask import url_for


def get_image_url(filename: str) -> str:
    return url_for("static", filename=f"uploads/{filename}", _external=True)
