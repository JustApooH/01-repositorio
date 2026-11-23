import os
import sqlite3
import tempfile
import unittest

from techflow.database import init_db
from techflow.repository import TaskRepository


class MigrationTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.db_path = os.path.join(tmp.name, "legacy.db")

    def create_legacy_database(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "CREATE TABLE tasks ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, "
            "description TEXT NOT NULL DEFAULT '', "
            "status TEXT NOT NULL DEFAULT 'todo', created_at TEXT NOT NULL)"
        )
        conn.execute(
            "INSERT INTO tasks (title, created_at) VALUES ('Antiga', '2024-01-01T00:00:00')"
        )
        conn.commit()
        conn.close()

    def test_banco_antigo_recebe_coluna_de_prioridade(self):
        self.create_legacy_database()
        repo = TaskRepository(self.db_path)
        task = repo.list_all()[0]
        self.assertEqual(task.title, "Antiga")
        self.assertEqual(task.priority, "medium")

    def test_inicializar_duas_vezes_nao_falha(self):
        init_db(self.db_path)
        init_db(self.db_path)
        self.assertEqual(TaskRepository(self.db_path).list_all(), [])


if __name__ == "__main__":
    unittest.main()
