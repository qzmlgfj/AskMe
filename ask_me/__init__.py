import os

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from sqlalchemy import text
import logging

from .extensions import db

from .blueprint.question_blueprint import question_bp
from .blueprint.auth_blueprint import auth_bp

from .version import __version__


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

    @app.route("/SKILL.md")
    def skill_md():
        """远程提供 AI 交互技能文档，供 Agent 直接拉取"""
        return send_from_directory(
            os.path.join(app.root_path, "skills"),
            "SKILL.md",
            mimetype="text/markdown",
        )

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
    check_schema(app)

    app.register_blueprint(question_bp)
    app.register_blueprint(auth_bp)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    db.init_app(app)


def check_schema(app):
    """确保表结构存在，并为存量库补齐新增列（SQLite 轻量迁移）"""
    with app.app_context():
        engine = db.engine
        insp = db.inspect(engine)
        tables = insp.get_table_names()
        if "admin" not in tables or "question" not in tables:
            db.create_all()
            insp = db.inspect(engine)
            tables = insp.get_table_names()
        if "question" not in tables:
            return
        # 存量库缺 ai_flags 列时补列（ALTER TABLE ADD COLUMN 常量默认值在 SQLite 下安全）
        columns = [c["name"] for c in insp.get_columns("question")]
        if "ai_flags" not in columns:
            try:
                db.session.execute(
                    text("ALTER TABLE question ADD COLUMN ai_flags INTEGER DEFAULT 0")
                )
                db.session.commit()
            except Exception as e:
                # 多 worker 并发启动时可能同时执行 ALTER，失败后重新确认列是否存在
                db.session.rollback()
                columns = [c["name"] for c in db.inspect(db.engine).get_columns("question")]
                if "ai_flags" not in columns:
                    raise e
