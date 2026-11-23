from flask import Blueprint, current_app, jsonify, render_template, request

from .models import PRIORITY_LABELS, STATUS_LABELS, Priority, Status
from .repository import TaskNotFound
from .validators import TaskValidator, ValidationError

bp = Blueprint("tasks", __name__)
validator = TaskValidator()


def repository():
    return current_app.extensions["task_repository"]


def read_filters():
    status = request.args.get("status") or None
    priority = request.args.get("priority") or None
    errors = {}
    if status and status not in Status.values():
        errors["status"] = "status deve ser todo, in_progress ou done"
    if priority and priority not in Priority.values():
        errors["priority"] = "prioridade deve ser low, medium, high ou critical"
    if errors:
        raise ValidationError(errors)
    return status, priority


@bp.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error="dados inválidos", details=error.errors), 400


@bp.errorhandler(TaskNotFound)
def handle_not_found(error):
    return jsonify(error="tarefa não encontrada"), 404


@bp.get("/")
def board():
    status, priority = read_filters()
    tasks = repository().list_all(status=status, priority=priority)
    columns = [
        {
            "key": status.value,
            "label": STATUS_LABELS[status.value],
            "tasks": [task for task in tasks if task.status == status.value],
        }
        for status in Status
    ]
    return render_template(
        "index.html",
        columns=columns,
        priority_labels=PRIORITY_LABELS,
        selected_priority=priority or "",
    )


@bp.get("/api/tasks")
def list_tasks():
    status, priority = read_filters()
    tasks = repository().list_all(status=status, priority=priority)
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
