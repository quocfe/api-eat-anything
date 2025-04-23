import os
from flask import Flask, Blueprint, jsonify, make_response
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_restx import Api
from sqlalchemy import event
from sqlalchemy.engine import Engine
from werkzeug.exceptions import BadRequest


# base_dir is the folder back 2 step
base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    # load only folder in apps
    modules = os.listdir(os.path.join(os.getcwd(), "apps"))
    listModule = []
    for module in modules:
        if os.path.isdir(os.path.join(os.getcwd(), "apps", module)):
            listModule.append(module)

    # create blueprint for api swagger
    api_bp = Blueprint("api", __name__, url_prefix="/api")

    authorizations = {
        "Bearer Token": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "**Bearer token**",
        }
    }

    api = Api(
        api_bp,
        version="1.0",
        title="Bviralbrand API",
        description="Bviralbrand API description",
        authorizations=authorizations,
        security="Bearer Token",
        validate=True,
    )

    for module_name in listModule:
        # check routes.py has in folder
        if os.path.isfile(os.path.join(os.getcwd(), "apps", module_name, "routes.py")):
            module = import_module("apps.{}.routes".format(module_name))
            app.register_blueprint(module.blueprint)

    # i want to create api from folder api in apps
    for module_name in listModule:
        api_path = os.path.join(os.getcwd(), "apps", module_name, "api.py")
        if os.path.isfile(api_path):
            module = import_module(f"apps.{module_name}.api")
            if hasattr(module, "ns"):
                api.add_namespace(module.ns)
    app.register_blueprint(api_bp)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print("> Error: DBMS Exception: " + str(e))

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            (print("oke", basedir))
            app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI = (
                "sqlite:///" + os.path.join(basedir, "db.sqlite3")
            )

            print("> Fallback to SQLite ")
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


# Enable foreign key constraints for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_app(config):
    templateFolder = os.path.join(base_dir, "templates")
    staticFolder = os.path.join(base_dir, "static")
    uploadFolder = os.path.join(staticFolder, "uploads")  # Define upload folder

    app = Flask(__name__, template_folder=templateFolder, static_folder=staticFolder)
    app.config.from_object(config)

    app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".jpeg", ".png"]
    app.config["UPLOAD_MIME_TYPES"] = ["image/jpeg", "image/jpg", "image/png"]
    app.config["UPLOAD_FOLDER"] = uploadFolder
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB limit

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
