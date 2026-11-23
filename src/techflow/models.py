from dataclasses import asdict, dataclass
from enum import Enum


class Status(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

    @classmethod
    def values(cls):
        return [item.value for item in cls]


STATUS_LABELS = {
    "todo": "A Fazer",
    "in_progress": "Em Progresso",
    "done": "Concluído",
}


@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str
    created_at: str

    @classmethod
    def from_row(cls, row):
        return cls(**{key: row[key] for key in row.keys()})

    def to_dict(self):
        return asdict(self)
