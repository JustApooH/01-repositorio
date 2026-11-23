from datetime import datetime, timezone

from .database import init_db, session
from .models import Task


class TaskNotFound(LookupError):
    pass


class TaskRepository:
    UPDATABLE = ("title", "description", "status")

    def __init__(self, db_path):
        self.db_path = db_path
        init_db(db_path)

    def create(self, title, description="", status="todo"):
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with session(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (title, description, status, created_at) "
                "VALUES (?, ?, ?, ?)",
                (title, description, status, created_at),
            )
            task_id = cursor.lastrowid
        return self.get(task_id)

    def get(self, task_id):
        with session(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
        if row is None:
            raise TaskNotFound(task_id)
        return Task.from_row(row)

    def list_all(self, status=None):
        query = "SELECT * FROM tasks"
        params = []
        if status:
            query += " WHERE status = ?"
            params.append(status)
        query += " ORDER BY id"
        with session(self.db_path) as conn:
            rows = conn.execute(query, params).fetchall()
        return [Task.from_row(row) for row in rows]

    def update(self, task_id, **fields):
        self.get(task_id)
        changes = {k: v for k, v in fields.items() if k in self.UPDATABLE}
        if changes:
            assignments = ", ".join(f"{column} = ?" for column in changes)
            with session(self.db_path) as conn:
                conn.execute(
                    f"UPDATE tasks SET {assignments} WHERE id = ?",
                    (*changes.values(), task_id),
                )
        return self.get(task_id)

    def delete(self, task_id):
        with session(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            deleted = cursor.rowcount
        if not deleted:
            raise TaskNotFound(task_id)
