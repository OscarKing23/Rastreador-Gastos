import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# --- Database Setup ---
conn = sqlite3.connect('expenses.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT,
    date TEXT
)
''')
conn.commit()
conn.close()

def get_db_connection():
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Routes ---
@app.route("/")
def index():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    total = conn.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
    conn.close()
    return render_template("index.html", expenses=expenses, total=total or 0)

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
            errors.append("Amount must be positive.")
    except (TypeError, ValueError):
        errors.append("Amount must be a valid number.")

    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
        (title, amount_val, category, date)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 201

@app.route("/expenses", methods=["GET"])
def get_expenses():
    conn = get_db_connection()
    expenses = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()
    data = [dict(row) for row in expenses]
    return jsonify({"status": "success", "data": data}), 200

@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)