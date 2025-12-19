// =========================
// Validation & Auth Logic (merged from login.js + signup.js)
// =========================

// Login Form
const loginEmailInput = document.getElementById('email');
const loginForm = document.getElementById('loginForm');
const loginPasswordInput = document.getElementById('password');
const loginSubmit = document.getElementById('submit');
const togglePassword = document.getElementById('togglePassword');

togglePassword?.addEventListener('click', () => {
  const isPassword = loginPasswordInput.type === "password";
  loginPasswordInput.type = isPassword ? "text" : "password";
  togglePassword.innerHTML = isPassword
    ? `<i class="fa-solid fa-eye-slash"></i>`
    : `<i class="fa-solid fa-eye"></i>`;
});

loginSubmit?.addEventListener('click', (e) => {
  e.preventDefault();
  const email = loginEmailInput.value.trim();
  const password = loginPasswordInput.value.trim();

  if (!email || !password) {
    alert("Please fill in all fields.");
    return;
  }

  const data = localStorage.getItem(`user_${email}`);
  if (!data) {
    alert("No account found. Please sign up first.");
    return;
  }

  const savedData = JSON.parse(data);
  if (savedData.password === password) {
    alert('Login successful!');
    localStorage.setItem('isLoggedIn', 'true');
    window.location.href = "/";
  } 
  else {
    alert('Incorrect password.');
  }
});

// Signup Form
const signupEmailInput = document.getElementById('email');
const signupForm = document.getElementById('loginForm');
const signupPasswordInput = document.getElementById('password');
const signupSubmit = document.getElementById('submit');

signupSubmit?.addEventListener('click', (e) => {
  e.preventDefault();
  const email = signupEmailInput.value.trim();
  const password = signupPasswordInput.value.trim();

  if (!email || !password) {
    alert("Please fill in all fields.");
    return;
  }

  const userData = { email, password };
  localStorage.setItem(`user_${email}`, JSON.stringify(userData));

  alert('Account created successfully!');
  window.location.href = "/login";
  signupForm.reset();
});

