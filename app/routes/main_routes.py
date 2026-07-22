from flask import Blueprint, render_template
from app.services.expense_service import ExpenseService

main_bp = Blueprint('main', __name__)
expense_service = ExpenseService()

@main_bp.route("/")
def index():
    """Ruta principal que renderiza la vista HTML."""
    expenses = expense_service.get_all_expenses()
    total = expense_service.get_total_expenses()
    return render_template("index.html", expenses=expenses, total=total)
