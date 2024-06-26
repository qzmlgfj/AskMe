import os

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import logging

from .extensions import db

from .blueprint.question_blueprint import question_bp
from .blueprint.auth_blueprint import auth_bp

__version__ = "1.2.0"


def create_app(*, is_test=False):
    """create and configure the app"""
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_folder="./dist/static",
        template_folder="./dist",
    )
    app.config.from_object("ask_me.config")

    try:
        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.INFO)
    except Exception as e:
        print(e)

    # if test_config is None:
    #   # load the instance config, if it exists, when not testing
    #   app.config.from_pyfile("config.py", silent=True)
    # else:
    #   # load the test config if passed in
    #   app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if is_test:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///" + app.instance_path + "/test.sqlite"
        )
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///" + app.instance_path + "/backend.sqlite"
        )

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"connect_args": {"timeout": 15}}

    @app.route("/favicon.png")
    def fav():
        return send_from_directory(os.path.join(app.root_path, "dist"), "favicon.png")

    @app.route("/", defaults={"path": ""})
    @app.route("/<string:path>")
    @app.route("/<path:path>")
    def catch_all(path):
        return render_template("index.html")

    @app.route("/api/version")
    def return_version():
        return __version__

    CORS(app)
    register_extensions(app)
    check_table_exists(app)

    app.register_blueprint(question_bp)
    app.register_blueprint(auth_bp)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)

def check_table_exists(app):
    with app.app_context():
        engine = db.get_engine()
        insp = db.inspect(engine)
        if "admin" not in insp.get_table_names():
            db.create_all()
