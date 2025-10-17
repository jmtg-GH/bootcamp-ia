const chatIcon = document.getElementById("chatbot-icon");
const chatContainer = document.getElementById("chat-container");
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// Estado del chat y del pedido
let chatVisible = false;
let pedido = [];
let direccion = "";

// Contenedor para quick replies (se inyecta)
let quickRepliesContainer = null;

// Abrir o cerrar el chatbot
chatIcon.addEventListener("click", () => {
  chatVisible = !chatVisible;
  if (chatVisible) chatContainer.classList.add("show");
  else {
    chatContainer.classList.remove("show");
    clearQuickReplies();
  }
});

// Agregar mensajes al chat (mejor formato)
function addMessage(sender, text) {
  const div = document.createElement("div");
  div.classList.add("message");
  // distinguir estilos por sender
  if (sender === "Tú") {
    div.innerHTML = `<strong>${sender}:</strong> <span class="msg-user">${escapeHtml(text)}</span>`;
    div.style.textAlign = "right";
  } else {
    div.innerHTML = `<strong>${sender}:</strong> <span class="msg-bot">${nl2br(escapeHtml(text))}</span>`;
  }
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// escapar HTML básico para seguridad
function escapeHtml(unsafe) {
  return String(unsafe || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
function nl2br(str) {
  return String(str).replace(/\n/g, "<br>");
}

// Crear / limpiar quick replies (botones para pago)
function ensureQuickRepliesContainer() {
  if (!quickRepliesContainer) {
    quickRepliesContainer = document.createElement("div");
    quickRepliesContainer.id = "quick-replies";
    quickRepliesContainer.style.display = "flex";
    quickRepliesContainer.style.gap = "8px";
    quickRepliesContainer.style.padding = "8px";
    quickRepliesContainer.style.justifyContent = "center";
    // Insertar antes del área de input
    const inputArea = document.querySelector(".chat-input-area");
    inputArea.parentNode.insertBefore(quickRepliesContainer, inputArea);
  }
}

function clearQuickReplies() {
  if (quickRepliesContainer) {
    quickRepliesContainer.remove();
    quickRepliesContainer = null;
  }
}

function showQuickReplies(options = []) {
  ensureQuickRepliesContainer();
  quickRepliesContainer.innerHTML = ""; // limpiar
  options.forEach(opt => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = opt.label;
    btn.dataset.value = opt.value;
    btn.style.padding = "6px 10px";
    btn.style.borderRadius = "8px";
    btn.style.border = "1px solid #e0e0e0";
    btn.style.background = "#fff";
    btn.style.cursor = "pointer";
    btn.addEventListener("click", async () => {
      // al hacer click se deshabilitan botones y se envía
      Array.from(quickRepliesContainer.children).forEach(b => b.disabled = true);
      await sendQuickReply(opt.value);
    });
    quickRepliesContainer.appendChild(btn);
  });
}

// Enviar mensaje al servidor (función principal)
async function enviarMensaje() {
  const mensaje = userInput.value.trim();
  if (!mensaje) return;

  addMessage("Tú", mensaje);
  userInput.value = "";
  clearQuickReplies();

  try {
    const resp = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mensaje: mensaje,
        pedido: pedido,
        direccion: direccion
      }),
    });

    if (!resp.ok) throw new Error("status " + resp.status);
    const data = await resp.json();

    addMessage("Bot", data.respuesta || "—");

    if (data.pedido) pedido = data.pedido;
    if (data.direccion) direccion = data.direccion;

    handleFase(data.fase, data);

  } catch (error) {
    addMessage("Bot", "⚠️ Error de conexión con el servidor.");
    console.error(error);
  }
}

// Enviar una respuesta rápida (por ejemplo 'efectivo')
async function sendQuickReply(value) {
  addMessage("Tú", value);
  clearQuickReplies();

  try {
    const resp = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        mensaje: value,
        pedido: pedido,
        direccion: direccion
      }),
    });

    if (!resp.ok) throw new Error("status " + resp.status);
    const data = await resp.json();

    addMessage("Bot", data.respuesta || "—");

    if (data.pedido) pedido = data.pedido;
    if (data.direccion) direccion = data.direccion;

    handleFase(data.fase, data);

  } catch (error) {
    addMessage("Bot", "⚠️ Error de conexión con el servidor.");
    console.error(error);
  }
}

// Manejar lógicas por fase (direccion, pago, final, inicio)
function handleFase(fase, data) {
  if (!fase) return;

  if (fase === "direccion") {
    addMessage("Bot", "Por favor indica tu dirección usando palabras como 'calle', 'cra', 'avenida', etc.");
  }

  else if (fase === "pago") {
    showQuickReplies([
      { label: "Efectivo", value: "efectivo" },
      { label: "Tarjeta", value: "tarjeta" },
      { label: "Transferencia", value: "transferencia" }
    ]);
  }

  else if (fase === "final") {
    const lastBotMsg = data.respuesta ? data.respuesta.toLowerCase() : "";
    if (!lastBotMsg.includes("en proceso") && !lastBotMsg.includes("proceso")) {
      addMessage("Bot", "🕒 Tu pedido está en proceso. Te avisaremos si hay novedades.");
    }
    if (!lastBotMsg.includes("gracias") && !lastBotMsg.includes("gracias por")) {
      addMessage("Bot", "💖 ¡Gracias por tu compra! Que disfrutes tu comida.");
    }

    // resetear estado local para permitir nuevos pedidos
    pedido = [];
    direccion = "";
    clearQuickReplies();
  }

  else if (fase === "inicio") {
    pedido = [];
    direccion = "";
    clearQuickReplies();
  }
}

// Botón y Enter
sendBtn.addEventListener("click", enviarMensaje);
userInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    enviarMensaje();
  }
});