// ===========================
// Toast Notification System
// ===========================
function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;

  const icon = type === 'success'
    ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="18" height="18"><polyline points="20 6 9 17 4 12"></polyline></svg>'
    : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" width="18" height="18"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>';

  toast.innerHTML = `${icon}<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('fade-out');
    toast.addEventListener('animationend', () => toast.remove());
  }, 3000);
}

// ===========================
// Dark Mode Toggle
// ===========================
function initDarkMode() {
  const toggle = document.getElementById('dark-mode-toggle');
  const savedTheme = localStorage.getItem('theme');

  if (savedTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  }

  toggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });
}

// ===========================
// Expenses CRUD
// ===========================
document.addEventListener('DOMContentLoaded', () => {
  initDarkMode();
  loadExpenses();

  document.getElementById('expense-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const expense = {
      title: document.getElementById('title').value,
      amount: document.getElementById('amount').value,
      category: document.getElementById('category').value,
      date: document.getElementById('date').value
    };

    fetch('/expenses', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(expense)
    })
      .then(response => {
        if (response.ok) {
          showToast('Expense added successfully!');
          this.reset();
          loadExpenses();
        } else {
          showToast('Failed to add expense.', 'error');
        }
      })
      .catch(() => showToast('Connection error.', 'error'));
  });
});

function loadExpenses() {
  fetch('/expenses')
    .then(response => response.json())
    .then(data => renderExpenses(data.data))
    .catch(() => showToast('Failed to load expenses.', 'error'));
}

function renderExpenses(expenses) {
  const tbody = document.querySelector('#expenses-table tbody');
  const emptyState = document.getElementById('empty-state');
  tbody.innerHTML = '';
  let total = 0;

  if (!expenses || expenses.length === 0) {
    emptyState.style.display = 'flex';
    document.querySelector('#expenses-table thead').style.display = 'none';
  } else {
    emptyState.style.display = 'none';
    document.querySelector('#expenses-table thead').style.display = '';

    expenses.forEach((expense, index) => {
      total += expense.amount;
      const row = document.createElement('tr');
      row.style.animation = `fadeInUp 0.3s ease ${index * 0.04}s both`;

      row.innerHTML = `
        <td>${expense.title}</td>
        <td>$${expense.amount.toFixed(2)}</td>
        <td><span class="category-tag">${expense.category || '—'}</span></td>
        <td>${expense.date || '—'}</td>
        <td>
          <button class="btn btn-danger" onclick="deleteExpense(${expense.id})">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"></path>
              <path d="M10 11v6"></path>
              <path d="M14 11v6"></path>
              <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"></path>
            </svg>
            Delete
          </button>
        </td>
      `;

      tbody.appendChild(row);
    });
  }

  document.getElementById('total').textContent = total.toFixed(2);
}

function deleteExpense(id) {
  fetch(`/expenses/${id}`, { method: 'DELETE' })
    .then(response => {
      if (response.ok) {
        showToast('Expense deleted.');
        loadExpenses();
      } else {
        showToast('Failed to delete expense.', 'error');
      }
    })
    .catch(() => showToast('Connection error.', 'error'));
}

function applyFilters() {
  const startDate = document.getElementById('start-date').value;
  const endDate = document.getElementById('end-date').value;
  const filterCategory = document.getElementById('filter-category').value.toLowerCase();

  fetch('/expenses')
    .then(response => response.json())
    .then(data => {
      let filtered = data.data;

      if (startDate && endDate) {
        filtered = filtered.filter(expense => {
          return expense.date >= startDate && expense.date <= endDate;
        });
      }
      if (filterCategory) {
        filtered = filtered.filter(expense =>
          expense.category.toLowerCase().includes(filterCategory)
        );
      }

      renderExpenses(filtered);
    })
    .catch(() => showToast('Failed to filter expenses.', 'error'));
}