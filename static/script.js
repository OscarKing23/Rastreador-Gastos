async function fetchExpenses() {
    const res = await fetch("/expenses");
    const data = await res.json();
    const tbody = document.querySelector("#expenses-table tbody");
    tbody.innerHTML = "";
    let total = 0;
    data.data.forEach(exp => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
  <td>${exp.title}</td>
  <td>${exp.amount}</td>
  <td>${exp.category}</td>
  <td>${exp.date}</td>
  <td><button class="delete-btn" data-index="${data.data.indexOf(exp)}">Delete</button></td>
`;
      tbody.appendChild(tr);
      total += exp.amount;
    });
    document.getElementById("total").textContent = total;
    document.querySelectorAll(".delete-btn").forEach(btn => {
        btn.addEventListener("click", async (e) => {
          const idx = e.currentTarget.getAttribute("data-index");
          const res = await fetch(`/expenses/${idx}`, { method: "DELETE" });
          const json = await res.json();
          if (res.ok && json.status === "success") {
            fetchExpenses(); // refresh table
          } else {
            alert(json.message || "Failed to delete expense.");
          }
        });
      });
  }
  
  document.getElementById("expense-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const expense = {
      title: document.getElementById("title").value,
      amount: document.getElementById("amount").value,
      category: document.getElementById("category").value,
      date: document.getElementById("date").value
    };
    await fetch("/expenses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(expense)
    });
    fetchExpenses();
    e.target.reset();

  });
  
  fetchExpenses();