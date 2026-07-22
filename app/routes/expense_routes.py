from flask import Blueprint, request, jsonify
from app.services.expense_service import ExpenseService

expenses_bp = Blueprint('expenses', __name__)
expense_service = ExpenseService()

@expenses_bp.route("/expenses", methods=["GET"])
def get_expenses():
    """Endpoint API para obtener el listado de gastos."""
    expenses = expense_service.get_all_expenses()
    return jsonify({"status": "success", "data": expenses}), 200

@expenses_bp.route("/expenses", methods=["POST"])
def add_expense():
    """Endpoint API para agregar un nuevo gasto."""
    data = request.get_json() or {}
    success, response, status_code = expense_service.create_expense(data)
    return jsonify(response), status_code

@expenses_bp.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    """Endpoint API para eliminar un gasto por ID."""
    success, response, status_code = expense_service.delete_expense(id)
    return jsonify(response), status_code
