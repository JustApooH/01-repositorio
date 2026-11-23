import unittest

from techflow.validators import (
    DESCRIPTION_MAX,
    TITLE_MAX,
    TaskValidator,
    ValidationError,
)


class TaskValidatorTests(unittest.TestCase):
    def setUp(self):
        self.validator = TaskValidator()

    def test_dados_validos_sao_limpos(self):
        result = self.validator.validate(
            {"title": "  Criar API  ", "description": " texto ", "status": "todo"}
        )
        self.assertEqual(
            result, {"title": "Criar API", "description": "texto", "status": "todo"}
        )

    def test_titulo_e_obrigatorio_na_criacao(self):
        with self.assertRaises(ValidationError) as ctx:
            self.validator.validate({})
        self.assertIn("title", ctx.exception.errors)

    def test_titulo_vazio_e_rejeitado(self):
        with self.assertRaises(ValidationError):
            self.validator.validate({"title": "   "})

    def test_titulo_nao_texto_e_rejeitado(self):
        with self.assertRaises(ValidationError):
            self.validator.validate({"title": 123})

    def test_titulo_muito_longo_e_rejeitado(self):
        with self.assertRaises(ValidationError):
            self.validator.validate({"title": "a" * (TITLE_MAX + 1)})

    def test_descricao_muito_longa_e_rejeitada(self):
        with self.assertRaises(ValidationError) as ctx:
            self.validator.validate(
                {"title": "ok", "description": "a" * (DESCRIPTION_MAX + 1)}
            )
        self.assertIn("description", ctx.exception.errors)

    def test_descricao_nao_texto_e_rejeitada(self):
        with self.assertRaises(ValidationError):
            self.validator.validate({"title": "ok", "description": 10})

    def test_status_invalido_e_rejeitado(self):
        with self.assertRaises(ValidationError) as ctx:
            self.validator.validate({"title": "ok", "status": "pendente"})
        self.assertIn("status", ctx.exception.errors)

    def test_atualizacao_parcial_nao_exige_titulo(self):
        result = self.validator.validate({"status": "done"}, partial=True)
        self.assertEqual(result, {"status": "done"})

    def test_corpo_que_nao_e_objeto_e_rejeitado(self):
        with self.assertRaises(ValidationError) as ctx:
            self.validator.validate(["title"])
        self.assertIn("body", ctx.exception.errors)


if __name__ == "__main__":
    unittest.main()
