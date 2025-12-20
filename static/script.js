async function fetchExpenses() {
    const res = await fetch("/expenses");
    const data = await res.json();
    const tbody = document.querySelector("#expenses-table tbody");
    tbody.innerHTML = "";
    let total = 0;
    data.data.forEach(exp => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${exp.title}</td><td>${exp.amount}</td><td>${exp.category}</td><td>${exp.date}</td>`;
      tbody.appendChild(tr);
      total += exp.amount;
    });
    document.getElementById("total").textContent = total;
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
  });
  
  fetchExpenses();