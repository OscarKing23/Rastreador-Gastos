from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Temporary in-memory storage
expenses = []

# POST /expenses → Add a new expense
@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    title = data.get("title", "").strip()
    amount = data.get("amount")
    category = data.get("category", "").strip()
    date = data.get("date", "").strip()

    errors = []
    if not title:
        errors.append("Title must not be empty.")
    try:
        amount_val = float(amount)
        if amount_val <= 0:
            errors.append("Amount must be a positive number.")
    except (TypeError, ValueError):
        errors.append("Amount must be a valid number.")

    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    expense = {
        "title": title,
        "amount": amount_val,
        "category": category,
        "date": date
    }
    expenses.append(expense)
    return jsonify({"status": "success", "data": expense}), 201

# GET /expenses → View all expenses
@app.route("/expenses", methods=["GET"])
def get_expenses():
    return jsonify({"status": "success", "data": expenses}), 200

# DELETE /expenses/<index> → Delete an expense
@app.route("/expenses/<int:index>", methods=["DELETE"])
def delete_expense(index):
    if 0 <= index < len(expenses):
        removed = expenses.pop(index)
        return jsonify({"status": "success", "data": removed}), 200
    return jsonify({"status": "error", "message": "Expense not found"}), 404

# Root route
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)