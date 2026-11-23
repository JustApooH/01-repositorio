import os
import tempfile
import unittest

from techflow.repository import TaskNotFound, TaskRepository


class TaskRepositoryTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = TaskRepository(os.path.join(tmp.name, "test.db"))

    def test_criar_retorna_tarefa_com_id_e_status_padrao(self):
        task = self.repo.create("Escrever testes")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Escrever testes")
        self.assertEqual(task.status, "todo")
        self.assertEqual(task.description, "")
        self.assertTrue(task.created_at)

    def test_buscar_tarefa_existente(self):
        created = self.repo.create("Tarefa", "descrição", "in_progress")
        found = self.repo.get(created.id)
        self.assertEqual(found, created)

    def test_buscar_tarefa_inexistente_levanta_erro(self):
        with self.assertRaises(TaskNotFound):
            self.repo.get(999)

    def test_listar_retorna_todas_em_ordem(self):
        self.repo.create("A")
        self.repo.create("B")
        titles = [t.title for t in self.repo.list_all()]
        self.assertEqual(titles, ["A", "B"])

    def test_listar_filtra_por_status(self):
        self.repo.create("A", status="todo")
        self.repo.create("B", status="done")
        done = self.repo.list_all(status="done")
        self.assertEqual([t.title for t in done], ["B"])

    def test_atualizar_altera_apenas_campos_informados(self):
        task = self.repo.create("Antigo", "desc")
        updated = self.repo.update(task.id, title="Novo")
        self.assertEqual(updated.title, "Novo")
        self.assertEqual(updated.description, "desc")

    def test_atualizar_ignora_campos_desconhecidos(self):
        task = self.repo.create("Tarefa")
        updated = self.repo.update(task.id, id=50, inexistente="x")
        self.assertEqual(updated.id, task.id)

    def test_atualizar_tarefa_inexistente_levanta_erro(self):
        with self.assertRaises(TaskNotFound):
            self.repo.update(42, title="x")

    def test_remover_apaga_tarefa(self):
        task = self.repo.create("Remover")
        self.repo.delete(task.id)
        self.assertEqual(self.repo.list_all(), [])

    def test_remover_tarefa_inexistente_levanta_erro(self):
        with self.assertRaises(TaskNotFound):
            self.repo.delete(7)


    def test_prioridade_padrao_e_media(self):
        self.assertEqual(self.repo.create("Tarefa").priority, "medium")

    def test_criar_com_prioridade_critica(self):
        self.assertEqual(self.repo.create("Urgente", priority="critical").priority, "critical")

    def test_atualizar_prioridade(self):
        task = self.repo.create("Tarefa")
        self.assertEqual(self.repo.update(task.id, priority="high").priority, "high")

    def test_listagem_ordena_por_prioridade(self):
        self.repo.create("baixa", priority="low")
        self.repo.create("critica", priority="critical")
        self.repo.create("media")
        self.repo.create("alta", priority="high")
        titles = [t.title for t in self.repo.list_all()]
        self.assertEqual(titles, ["critica", "alta", "media", "baixa"])

    def test_listagem_filtra_por_prioridade_e_status(self):
        self.repo.create("A", status="done", priority="critical")
        self.repo.create("B", status="todo", priority="critical")
        self.repo.create("C", status="done", priority="low")
        result = self.repo.list_all(status="done", priority="critical")
        self.assertEqual([t.title for t in result], ["A"])


if __name__ == "__main__":
    unittest.main()
