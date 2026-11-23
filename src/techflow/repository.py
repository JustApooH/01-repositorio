from datetime import datetime, timezone

from .database import init_db, session
from .models import Task


class TaskNotFound(LookupError):
    pass


class TaskRepository:
    UPDATABLE = ("title", "description", "status", "priority")
    PRIORITY_ORDER = (
        "CASE priority WHEN 'critical' THEN 0 WHEN 'high' THEN 1 "
        "WHEN 'medium' THEN 2 ELSE 3 END"
    )

    def __init__(self, db_path):
        self.db_path = db_path
        init_db(db_path)

    def create(self, title, description="", status="todo", priority="medium"):
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with session(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (title, description, status, priority, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (title, description, status, priority, created_at),
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

    def list_all(self, status=None, priority=None):
        query = "SELECT * FROM tasks"
        filters = []
        params = []
        if status:
            filters.append("status = ?")
            params.append(status)
        if priority:
            filters.append("priority = ?")
            params.append(priority)
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += f" ORDER BY {self.PRIORITY_ORDER}, id"
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
