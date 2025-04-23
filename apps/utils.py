from mimetypes import guess_type
import re
import unicodedata
from flask import jsonify, current_app
import os
import datetime
from werkzeug.utils import secure_filename
from flask import flash


def res_data(data=[], msg="success", code=200, **kwargs):
    if code == 200:
        if len(data) > 0:
            result = {"msg": msg, "data": data, "code": code}
        else:
            result = {"msg": msg, "code": code}
    else:
        result = {"msg": msg, "code": code}
    if kwargs:
        for key, value in kwargs.items():
            result[key] = value
    print(result)
    # return jsonify(result), code
    return result, code


def slugify(text):
    # Chuyển thành Unicode chuẩn
    text = unicodedata.normalize("NFKD", text)

    # Loại bỏ dấu tiếng Việt (hoặc accent khác)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Lowercase, bỏ ký tự không cần thiết
    text = re.sub(r"[^\w\s-]", "", text.lower())

    # Thay khoảng trắng hoặc dấu gạch dưới thành dấu gạch ngang
    text = re.sub(r"[\s_-]+", "-", text).strip("-")

    return text


def is_allowed_file(file):
    if not file or file.filename.strip() == "":
        return False

    ext = os.path.splitext(file.filename)[1].lower()
    mime_type, _ = guess_type(file.filename)

    allowed_exts = current_app.config.get("UPLOAD_EXTENSIONS", [])
    allowed_mimes = current_app.config.get("UPLOAD_MIME_TYPES", [])

    return ext in allowed_exts and mime_type in allowed_mimes


def handle_file_upload(file, filename_prefix):
    if not is_allowed_file(file):
        return flash(f"File is not allowed", "danger")

    ext = os.path.splitext(file.filename)[1].lower()
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    filename = f"{filename_prefix}-{current_date}{ext}"
    filename = secure_filename(filename)

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    upload_path = os.path.join(upload_folder, filename)
    file.save(upload_path)
    return filename


def delete_file_if_exists(filename):
    if not filename:
        return

    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {filename}: {e}")
