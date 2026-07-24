"""Tests for the ExpenseService business logic layer."""
from app.services.expense_service import ExpenseService


class TestExpenseServiceGetAll:
    """Tests for ExpenseService.get_all_expenses."""

    def test_service_get_all_empty(self, app):
        """Service should return an empty list on a clean database."""
        with app.app_context():
            service = ExpenseService()
            expenses = service.get_all_expenses()
            assert expenses == []


class TestExpenseServiceCreate:
    """Tests for ExpenseService.create_expense."""

    def test_service_create_expense(self, app):
        """Service should successfully create an expense and return its dict."""
        with app.app_context():
            service = ExpenseService()
            success, response, status = service.create_expense({
                "title": "Coffee",
                "amount": 4.50,
                "category": "Drinks",
                "date": "2025-07-20"
            })
            assert success is True
            assert status == 201
            assert response["data"]["title"] == "Coffee"
            assert response["data"]["amount"] == 4.50

    def test_service_create_no_data(self, app):
        """Service should reject None or empty data with a 400 error."""
        with app.app_context():
            service = ExpenseService()
            success, response, status = service.create_expense(None)
            assert success is False
            assert status == 400


class TestExpenseServiceDelete:
    """Tests for ExpenseService.delete_expense."""

    def test_service_delete_nonexistent(self, app):
        """Service should return failure when deleting a non-existent ID."""
        with app.app_context():
            service = ExpenseService()
            success, response, status = service.delete_expense(99999)
            assert success is False
            assert status == 404


class TestExpenseServiceTotal:
    """Tests for ExpenseService.get_total_expenses."""

    def test_service_get_total(self, app):
        """Service should return the correct sum of all expense amounts."""
        with app.app_context():
            service = ExpenseService()
            service.create_expense({
                "title": "Item A",
                "amount": 10.00,
                "category": "Test",
                "date": "2025-01-01"
            })
            service.create_expense({
                "title": "Item B",
                "amount": 25.50,
                "category": "Test",
                "date": "2025-01-02"
            })
            total = service.get_total_expenses()
            assert total == 35.50
