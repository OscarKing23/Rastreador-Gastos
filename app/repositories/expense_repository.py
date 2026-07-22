from typing import List, Optional
from app.database import get_db_connection
from app.models.expense import Expense

class ExpenseRepository:
    """Repositorio para gestionar la persistencia y consultas de la entidad Expense."""

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path

    def get_all(self) -> List[Expense]:
        """Recupera todos los gastos ordenados por ID."""
        conn = get_db_connection(self.db_path)
        rows = conn.execute("SELECT * FROM expenses ORDER BY id ASC").fetchall()
        conn.close()
        return [Expense.from_row(row) for row in rows]

    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        """Busca un gasto por su identificador único."""
        conn = get_db_connection(self.db_path)
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
        conn.close()
        return Expense.from_row(row) if row else None

    def create(self, title: str, amount: float, category: str, date: str) -> Expense:
        """Inserta un nuevo gasto en la base de datos."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
            (title, amount, category, date)
        )
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return Expense(id=expense_id, title=title, amount=amount, category=category, date=date)

    def delete(self, expense_id: int) -> bool:
        """Elimina un gasto por su identificador."""
        conn = get_db_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted_count > 0

    def get_total(self) -> float:
        """Calcula el total sumado de los gastos."""
        conn = get_db_connection(self.db_path)
        result = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
        conn.close()
        return result or 0.0
