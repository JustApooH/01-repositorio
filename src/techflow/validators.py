from .models import Priority, Status

TITLE_MAX = 100
DESCRIPTION_MAX = 500


class ValidationError(ValueError):
    def __init__(self, errors):
        super().__init__("dados inválidos")
        self.errors = errors


class TaskValidator:
    def validate(self, data, partial=False):
        if not isinstance(data, dict):
            raise ValidationError({"body": "o corpo deve ser um objeto JSON"})

        errors = {}
        cleaned = {}

        if "title" in data or not partial:
            title = data.get("title")
            if not isinstance(title, str) or not title.strip():
                errors["title"] = "título é obrigatório"
            elif len(title.strip()) > TITLE_MAX:
                errors["title"] = f"título deve ter no máximo {TITLE_MAX} caracteres"
            else:
                cleaned["title"] = title.strip()

        if "description" in data:
            description = data["description"]
            if not isinstance(description, str):
                errors["description"] = "descrição deve ser um texto"
            elif len(description.strip()) > DESCRIPTION_MAX:
                errors["description"] = (
                    f"descrição deve ter no máximo {DESCRIPTION_MAX} caracteres"
                )
            else:
                cleaned["description"] = description.strip()

        if "status" in data:
            if data["status"] not in Status.values():
                errors["status"] = "status deve ser todo, in_progress ou done"
            else:
                cleaned["status"] = data["status"]

        if "priority" in data:
            if data["priority"] not in Priority.values():
                errors["priority"] = "prioridade deve ser low, medium, high ou critical"
            else:
                cleaned["priority"] = data["priority"]

        if errors:
            raise ValidationError(errors)
        return cleaned
