document.addEventListener("DOMContentLoaded", () => {
    loadExpenses();
  
    document.getElementById("expense-form").addEventListener("submit", function(e) {
      e.preventDefault();
  
      const expense = {
        title: document.getElementById("title").value,
        amount: document.getElementById("amount").value,
        category: document.getElementById("category").value,
        date: document.getElementById("date").value
      };
  
      fetch("/expenses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(expense)
      })
      .then(response => {
        if (response.ok) {
          alert("Expense added successfully!");
          this.reset();
          loadExpenses();
        } else {
          alert("Failed to add expense.");
        }
      });
    });
  });
  
  function loadExpenses() {
    fetch("/expenses")
      .then(response => response.json())
      .then(data => {
        const tbody = document.querySelector("#expenses-table tbody");
        tbody.innerHTML = "";
        let total = 0;
  
        data.data.forEach(expense => {
          total += expense.amount;
          const row = document.createElement("tr");
  
          row.innerHTML = `
            <td>${expense.title}</td>
            <td>${expense.amount}</td>
            <td>${expense.category}</td>
            <td>${expense.date}</td>
            <td><button onclick="deleteExpense(${expense.id})">Delete</button></td>
          `;
  
          tbody.appendChild(row);
        });
  
        document.getElementById("total").textContent = total.toFixed(2);
      });
  }
  
  function deleteExpense(id) {
    fetch(`/expenses/${id}`, { method: "DELETE" })
      .then(response => {
        if (response.ok) {
          alert("Expense deleted successfully!");
          loadExpenses();
        } else {
          alert("Failed to delete expense.");
        }
      });
  }