from dataclasses import dataclass
from typing import Optional

@dataclass
class Expense:
    """Modelo de dominio para un gasto."""
    id: Optional[int]
    title: str
    amount: float
    category: str
    date: str

    def to_dict(self) -> dict:
        """Convierte el modelo a un diccionario serializable a JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    @classmethod
    def from_row(cls, row) -> "Expense":
        """Construye una instancia de Expense a partir de un Row de SQLite."""
        return cls(
            id=row["id"],
            title=row["title"],
            amount=row["amount"],
            category=row["category"] if row["category"] is not None else "",
            date=row["date"] if row["date"] is not None else ""
        )
