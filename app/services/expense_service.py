from typing import Tuple, List, Dict, Any, Optional
from app.repositories.expense_repository import ExpenseRepository
from app.models.expense import Expense

class ExpenseService:
    """Servicio de negocio para la gestión y validación de gastos."""

    def __init__(self, repository: Optional[ExpenseRepository] = None):
        self.repository = repository or ExpenseRepository()

    def get_all_expenses(self) -> List[Dict[str, Any]]:
        """Obtiene todos los gastos en formato diccionario."""
        expenses = self.repository.get_all()
        return [expense.to_dict() for expense in expenses]

    def get_total_expenses(self) -> float:
        """Obtiene la suma total de gastos."""
        return self.repository.get_total()

    def create_expense(self, data: Dict[str, Any]) -> Tuple[bool, Any, int]:
        """Valida y crea un nuevo gasto."""
        if not data:
            return False, {"errors": ["Datos incompletos."]}, 400

        title = str(data.get("title", "")).strip()
        amount = data.get("amount")
        category = str(data.get("category", "")).strip()
        date = str(data.get("date", "")).strip()

        errors = []
        if not title:
            errors.append("Title must not be empty.")

        try:
            amount_val = float(amount)
            if amount_val <= 0:
                errors.append("Amount must be positive.")
        except (TypeError, ValueError):
            errors.append("Amount must be a valid number.")

        if errors:
            return False, {"status": "error", "errors": errors}, 400

        expense = self.repository.create(title, amount_val, category, date)
        return True, {"status": "success", "data": expense.to_dict()}, 201

    def delete_expense(self, expense_id: int) -> Tuple[bool, Any, int]:
        """Elimina un gasto por ID."""
        success = self.repository.delete(expense_id)
        if success:
            return True, {"status": "deleted"}, 200
        else:
            return False, {"status": "error", "message": "Expense not found"}, 404
