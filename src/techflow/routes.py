from flask import Blueprint, current_app, jsonify, render_template, request

from .models import STATUS_LABELS, Status
from .repository import TaskNotFound
from .validators import TaskValidator, ValidationError

bp = Blueprint("tasks", __name__)
validator = TaskValidator()


def repository():
    return current_app.extensions["task_repository"]


@bp.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error="dados inválidos", details=error.errors), 400


@bp.errorhandler(TaskNotFound)
def handle_not_found(error):
    return jsonify(error="tarefa não encontrada"), 404


@bp.get("/")
def board():
    tasks = repository().list_all()
    columns = [
        {
            "key": status.value,
            "label": STATUS_LABELS[status.value],
            "tasks": [task for task in tasks if task.status == status.value],
        }
        for status in Status
    ]
    return render_template("index.html", columns=columns)


@bp.get("/api/tasks")
def list_tasks():
    status = request.args.get("status")
    if status and status not in Status.values():
        raise ValidationError({"status": "status deve ser todo, in_progress ou done"})
    tasks = repository().list_all(status=status)
    return jsonify([task.to_dict() for task in tasks])


@bp.post("/api/tasks")
def create_task():
    data = validator.validate(request.get_json(silent=True))
    task = repository().create(**data)
    return jsonify(task.to_dict()), 201


@bp.get("/api/tasks/<int:task_id>")
def get_task(task_id):
    return jsonify(repository().get(task_id).to_dict())


@bp.put("/api/tasks/<int:task_id>")
def update_task(task_id):
    data = validator.validate(request.get_json(silent=True), partial=True)
    task = repository().update(task_id, **data)
    return jsonify(task.to_dict())


@bp.delete("/api/tasks/<int:task_id>")
def delete_task(task_id):
    repository().delete(task_id)
    return "", 204
