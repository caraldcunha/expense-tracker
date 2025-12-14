// =========================
// Main App Logic (merged from script.js + expenses.js)
// =========================

// DOM Elements
const date = document.getElementById('date');
const description = document.getElementById('description');
const category = document.getElementById('category');
const amount = document.getElementById('amount');
const addBtn = document.getElementById('add');

const incomeEl = document.getElementById('income');
const totalExpenseEl = document.getElementById('total-expense');
const remainingBalanceEl = document.getElementById('reme-balance');
const transactionsBody = document.getElementById('transactionsBody');

const ul = document.querySelector('ul');
const menuIcon = document.querySelector('.menu-icon');

// ------------------- Menu Toggle -------------------
let menuVisible = false;
menuIcon.addEventListener('click', () => {
  ul.style.visibility = menuVisible ? "hidden" : "visible";
  menuVisible = !menuVisible;
});

// ------------------- Chart Setup -------------------
const ctx = document.getElementById('categoryChart')?.getContext('2d');
const categoryLabels = ['Food', 'Travel', 'Utilities', 'Entertainment'];

const chartData = {
  labels: categoryLabels,
  datasets: [{
    label: 'Expenses',
    data: [0, 0, 0, 0],
    backgroundColor: ['#4F46E5', '#22C55E', '#FACC15', '#EF4444'],
    borderWidth: 1
  }]
};

let categoryChart;
if (ctx) {
  categoryChart = new Chart(ctx, {
    type: 'doughnut',
    data: chartData,
    options: {
      responsive: true,
      plugins: { legend: { position: 'bottom' } }
    }
  });
}

// ------------------- State -------------------
let expenses = [];
let totalIncome = parseFloat(localStorage.getItem('totalIncome')) || 0;

// ------------------- On Page Load -------------------
window.addEventListener('DOMContentLoaded', () => {
  const savedExpenses = localStorage.getItem('expenses');
  if (savedExpenses) {
    expenses = JSON.parse(savedExpenses).map(exp => ({
      ...exp,
      amount: parseFloat(exp.amount) || 0
    }));
    expenses.forEach(addExpenseToTable);
    updateBalances();
    updateChartData();
  }

  // Initialize income and balances
  incomeEl.textContent = `$${totalIncome.toFixed(2)}`;
  const storedRemaining = parseFloat(localStorage.getItem('remainingBalance'));
  const remaining = isNaN(storedRemaining) ? totalIncome : storedRemaining;
  remainingBalanceEl.textContent = `$${remaining.toFixed(2)}`;
});

// ------------------- Income Setter -------------------
incomeEl?.addEventListener('click', () => {
  const newIncomeStr = prompt("Enter your monthly income:", totalIncome || 0);
  if (newIncomeStr !== null) {
    const newIncome = parseFloat(newIncomeStr);
    if (!isNaN(newIncome) && newIncome >= 0) {
      totalIncome = newIncome;
      localStorage.setItem('totalIncome', totalIncome.toFixed(2));
      updateBalances();
    } else {
      alert("Please enter a valid number for income.");
    }
  }
});

// ------------------- Add Expense -------------------
addBtn?.addEventListener('click', () => {
  const expeDate = date.value.trim();
  const expeDescription = description.value.trim();
  const expeCategory = category.value.trim();
  const expeAmount = amount.value.trim();

  if (!expeDate || !expeDescription || !expeCategory || !expeAmount) {
    alert("Please fill in all fields.");
    return;
  }

  const expense = {
    date: expeDate,
    description: expeDescription,
    category: expeCategory,
    amount: parseFloat(expeAmount)
  };

  expenses.push(expense);
  localStorage.setItem('expenses', JSON.stringify(expenses));

  addExpenseToTable(expense);
  updateBalances();
  updateChartData();

  // Clear form
  date.value = "";
  description.value = "";
  category.value = "";
  amount.value = "";
});

// ------------------- Add Expense Row -------------------
function addExpenseToTable(expense) {
  const amountNum = parseFloat(expense.amount) || 0;
  const row = document.createElement('tr');
  row.innerHTML = `
    <td>${expense.date}</td>
    <td>${expense.description}</td>
    <td>${expense.category}</td>
    <td class="negative">-$${amountNum.toFixed(2)}</td>
  `;
  transactionsBody.appendChild(row);
}

// ------------------- Balance Calculation -------------------
function updateBalances() {
  const totalExpense = expenses.reduce((sum, e) => sum + (parseFloat(e.amount) || 0), 0);
  const remaining = totalIncome - totalExpense;

  incomeEl.textContent = `$${totalIncome.toFixed(2)}`;
  totalExpenseEl.textContent = `$${totalExpense.toFixed(2)}`;
  remainingBalanceEl.textContent = `$${remaining.toFixed(2)}`;

  localStorage.setItem('remainingBalance', remaining.toFixed(2));
}

// ------------------- Chart Update -------------------
function updateChartData() {
  if (!categoryChart) return;
  const categorySums = { Food: 0, Travel: 0, Utilities: 0, Entertainment: 0 };

  expenses.forEach(exp => {
    const amountNum = parseFloat(exp.amount) || 0;
    if (categorySums.hasOwnProperty(exp.category)) {
      categorySums[exp.category] += amountNum;
    }
  });

  chartData.datasets[0].data = categoryLabels.map(cat => categorySums[cat]);
  categoryChart.update();
}

