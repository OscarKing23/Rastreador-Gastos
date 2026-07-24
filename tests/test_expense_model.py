"""Tests for the Expense data model."""
from app.models.expense import Expense


class TestExpenseToDict:
    """Tests for Expense.to_dict serialization."""

    def test_expense_to_dict(self):
        """to_dict() should return a dictionary with all expected keys and values."""
        expense = Expense(id=1, title="Lunch", amount=15.00, category="Food", date="2025-07-20")
        result = expense.to_dict()
        assert result == {
            "id": 1,
            "title": "Lunch",
            "amount": 15.00,
            "category": "Food",
            "date": "2025-07-20"
        }


class TestExpenseFromRow:
    """Tests for Expense.from_row construction."""

    def test_expense_from_row(self):
        """from_row() should construct a valid Expense from a dict-like row."""
        # Simulate a sqlite3.Row using a dict with key access
        class FakeRow:
            def __init__(self, data):
                self._data = data
            def __getitem__(self, key):
                return self._data[key]

        row = FakeRow({
            "id": 42,
            "title": "Taxi",
            "amount": 8.75,
            "category": "Transport",
            "date": "2025-07-21"
        })
        expense = Expense.from_row(row)
        assert expense.id == 42
        assert expense.title == "Taxi"
        assert expense.amount == 8.75
        assert expense.category == "Transport"
        assert expense.date == "2025-07-21"
