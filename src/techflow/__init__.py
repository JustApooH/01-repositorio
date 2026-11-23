import os

from flask import Flask

from .repository import TaskRepository
from .routes import bp


def create_app(db_path=None):
    app = Flask(__name__)
    path = db_path or os.environ.get("TECHFLOW_DB", "techflow.db")
    app.extensions["task_repository"] = TaskRepository(path)
    app.register_blueprint(bp)
    return app
