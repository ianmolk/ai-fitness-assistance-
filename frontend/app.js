// frontend/app.js
const API = "http://127.0.0.1:8001";

// ---------- helpers ----------
function escapeHtml(text) {
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
  return String(text).replace(/[&<>"']/g, (m) => map[m]);
}

function getToken() {
  return localStorage.getItem("token"); // stored during login()
}

function setStatus(id, msg) {
  const el = document.getElementById(id);
  if (el) el.textContent = msg;
}

// ---------- AUTH (login/register page) ----------
async function register() {
  const email = document.getElementById("regEmail")?.value || "";
  const password = document.getElementById("regPassword")?.value || "";
  const status = document.getElementById("registerStatus");

  try {
    const res = await fetch(`${API}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      status.textContent = data.error || data.detail || "Registration failed";
      return;
    }
    status.textContent = "Account created! You can now log in.";
  } catch (error) {
    console.error("Registration error:", error);
    status.textContent = "Backend not running. Start backend on port 8001.";
  }
}

async function login() {
  const email = document.getElementById("loginEmail")?.value || "";
  const password = document.getElementById("loginPassword")?.value || "";
  const status = document.getElementById("loginStatus");

  try {
    const res = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      status.textContent = data.error || data.detail || "Login failed";
      return;
    }

    // backend might return: { token: "..." } OR { access_token: "..." }
    const token = data.token || data.access_token;
    if (!token) {
      status.textContent = "Login worked, but no token returned by backend.";
      return;
    }

    localStorage.setItem("token", token);
    status.textContent = "Login successful!";
    setTimeout(() => (window.location.href = "index.html"), 500);
  } catch (error) {
    console.error("Login error:", error);
    status.textContent = "Backend not running. Start backend on port 8001.";
  }
}

// expose for onclick="login()" / onclick="register()"
window.login = login;
window.register = register;

// ---------- CHAT (chat.html) ----------
async function sendMessage() {
  const input = document.getElementById("messageInput");
  const chatContainer = document.getElementById("chatContainer");

  if (!input || !chatContainer) {
    console.error("Chat elements not found. Are you on chat.html?");
    return;
  }

  const message = (input.value || "").trim();
  if (!message) return;

  // add user bubble
  const userMsgDiv = document.createElement("div");
  userMsgDiv.className = "chat-message user";
  userMsgDiv.innerHTML = `<div class="message-bubble user">${escapeHtml(message)}</div>`;
  chatContainer.appendChild(userMsgDiv);

  // add temporary bot bubble
  const botMsgDiv = document.createElement("div");
  botMsgDiv.className = "chat-message";
  botMsgDiv.innerHTML = `<div class="message-bubble bot">Thinking...</div>`;
  chatContainer.appendChild(botMsgDiv);

  chatContainer.scrollTop = chatContainer.scrollHeight;
  input.value = "";

  // call backend
  try {
    const token = getToken();
    if (!token) {
      botMsgDiv.innerHTML = `<div class="message-bubble bot">You are not logged in. Go to login.html and login first.</div>`;
      return;
    }

    const res = await fetch(`${API}/chat/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ message }),
    });

    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      const errMsg = data.error || data.detail || `Request failed (${res.status})`;
      botMsgDiv.innerHTML = `<div class="message-bubble bot">${escapeHtml(errMsg)}</div>`;
      return;
    }

    // backend might return: { reply: "..." } OR { message: "..." }
    const reply = data.reply || data.message || JSON.stringify(data);
    // Replace newlines with <br> for better formatting
    const formattedReply = escapeHtml(reply).replace(/\n/g, '<br>');
    botMsgDiv.innerHTML = `<div class="message-bubble bot">${formattedReply}</div>`;
  } catch (error) {
    console.error("Chat error:", error);
    botMsgDiv.innerHTML = `<div class="message-bubble bot">Could not reach backend. Is it running on port 8001?</div>`;
  } finally {
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }
}

// IMPORTANT: make it global so chat.html onclick="sendMessage()" works
window.sendMessage = sendMessage;
