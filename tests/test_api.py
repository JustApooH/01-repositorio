import os
import tempfile
import unittest

from techflow import create_app


class TaskApiTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        app = create_app(os.path.join(tmp.name, "api.db"))
        app.testing = True
        self.client = app.test_client()

    def create(self, **payload):
        return self.client.post("/api/tasks", json=payload)

    def test_criar_tarefa_retorna_201(self):
        response = self.create(title="Nova tarefa", description="detalhe")
        self.assertEqual(response.status_code, 201)
        body = response.get_json()
        self.assertEqual(body["title"], "Nova tarefa")
        self.assertEqual(body["status"], "todo")

    def test_criar_sem_titulo_retorna_400(self):
        response = self.create(description="sem título")
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.get_json()["details"])

    def test_criar_com_corpo_invalido_retorna_400(self):
        response = self.client.post("/api/tasks", data="texto", content_type="text/plain")
        self.assertEqual(response.status_code, 400)

    def test_listar_retorna_tarefas_criadas(self):
        self.create(title="A")
        self.create(title="B")
        response = self.client.get("/api/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual([t["title"] for t in response.get_json()], ["A", "B"])

    def test_listar_filtra_por_status(self):
        self.create(title="A", status="done")
        self.create(title="B")
        response = self.client.get("/api/tasks?status=done")
        self.assertEqual([t["title"] for t in response.get_json()], ["A"])

    def test_listar_com_status_invalido_retorna_400(self):
        response = self.client.get("/api/tasks?status=xyz")
        self.assertEqual(response.status_code, 400)

    def test_buscar_tarefa_por_id(self):
        task_id = self.create(title="Buscar").get_json()["id"]
        response = self.client.get(f"/api/tasks/{task_id}")
        self.assertEqual(response.get_json()["title"], "Buscar")

    def test_buscar_inexistente_retorna_404(self):
        self.assertEqual(self.client.get("/api/tasks/99").status_code, 404)

    def test_atualizar_status_da_tarefa(self):
        task_id = self.create(title="Mover").get_json()["id"]
        response = self.client.put(f"/api/tasks/{task_id}", json={"status": "in_progress"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "in_progress")

    def test_atualizar_com_dado_invalido_retorna_400(self):
        task_id = self.create(title="Mover").get_json()["id"]
        response = self.client.put(f"/api/tasks/{task_id}", json={"status": "voando"})
        self.assertEqual(response.status_code, 400)

    def test_atualizar_inexistente_retorna_404(self):
        response = self.client.put("/api/tasks/99", json={"title": "x"})
        self.assertEqual(response.status_code, 404)

    def test_remover_tarefa_retorna_204(self):
        task_id = self.create(title="Remover").get_json()["id"]
        self.assertEqual(self.client.delete(f"/api/tasks/{task_id}").status_code, 204)
        self.assertEqual(self.client.get(f"/api/tasks/{task_id}").status_code, 404)

    def test_remover_inexistente_retorna_404(self):
        self.assertEqual(self.client.delete("/api/tasks/99").status_code, 404)

    def test_quadro_exibe_colunas_e_tarefas(self):
        self.create(title="Visível no quadro")
        response = self.client.get("/")
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("A Fazer", html)
        self.assertIn("Em Progresso", html)
        self.assertIn("Concluído", html)
        self.assertIn("Visível no quadro", html)


    def test_criar_com_prioridade(self):
        response = self.create(title="Urgente", priority="critical")
        self.assertEqual(response.get_json()["priority"], "critical")

    def test_prioridade_padrao_na_api(self):
        self.assertEqual(self.create(title="Normal").get_json()["priority"], "medium")

    def test_criar_com_prioridade_invalida_retorna_400(self):
        response = self.create(title="Erro", priority="nenhuma")
        self.assertEqual(response.status_code, 400)
        self.assertIn("priority", response.get_json()["details"])

    def test_listar_ordenado_e_filtrado_por_prioridade(self):
        self.create(title="baixa", priority="low")
        self.create(title="critica", priority="critical")
        ordered = self.client.get("/api/tasks").get_json()
        self.assertEqual([t["title"] for t in ordered], ["critica", "baixa"])
        filtered = self.client.get("/api/tasks?priority=low").get_json()
        self.assertEqual([t["title"] for t in filtered], ["baixa"])

    def test_filtro_de_prioridade_invalido_retorna_400(self):
        self.assertEqual(self.client.get("/api/tasks?priority=xyz").status_code, 400)

    def test_quadro_filtra_por_prioridade(self):
        self.create(title="Tarefa crítica", priority="critical")
        self.create(title="Tarefa baixa", priority="low")
        html = self.client.get("/?priority=critical").get_data(as_text=True)
        self.assertIn("Tarefa crítica", html)
        self.assertNotIn("Tarefa baixa", html)


if __name__ == "__main__":
    unittest.main()
