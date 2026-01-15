 const API = "http://127.0.0.1:8001";

async function register() {
  const email = document.getElementById("regEmail").value;
  const password = document.getElementById("regPassword").value;
  const status = document.getElementById("registerStatus");

  try {
    const res = await fetch(`${API}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();
    if (!res.ok) {
      status.textContent = data.detail || "Registration failed";
      return;
    }
    status.textContent = "Account created! You can now log in.";
  } catch (error) {
    console.error("Registration error:", error);
    status.textContent = "Backend not running. Make sure to run: python -m uvicorn app:app --reload --port 8001";
  }
}

async function login() {
  const email = document.getElementById("loginEmail").value;
  const password = document.getElementById("loginPassword").value;
  const status = document.getElementById("loginStatus");

  try {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();
    if (!res.ok) {
      status.textContent = data.detail || "Login failed";
      return;
    }

    localStorage.setItem("token", data.access_token);
    status.textContent = "Login successful!";
    setTimeout(() => window.location.href = "index.html", 800);
  } catch (error) {
    console.error("Login error:", error);
    status.textContent = "Backend not running. Make sure to run: python -m uvicorn app:app --reload --port 8001";
  }
}
