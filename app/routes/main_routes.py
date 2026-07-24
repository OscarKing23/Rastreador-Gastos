from datetime import datetime, timezone
from flask import Blueprint, render_template, jsonify
from app.services.expense_service import ExpenseService
from app.database import get_db_connection

main_bp = Blueprint('main', __name__)
expense_service = ExpenseService()

@main_bp.route("/")
def index():
    """Ruta principal que renderiza la vista HTML."""
    expenses = expense_service.get_all_expenses()
    total = expense_service.get_total_expenses()
    return render_template("index.html", expenses=expenses, total=total)

@main_bp.route("/api/health", methods=["GET"])
def health_check():
    """Endpoint de diagnóstico para monitorear la salud del servidor en tiempo real."""
    db_status = "connected"
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1")
        conn.close()
    except Exception as e:
        db_status = f"error: {str(e)}"

    status_code = 200 if db_status == "connected" else 500
    return jsonify({
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), status_code

