document.addEventListener("DOMContentLoaded", () => {
    const chatIcon = document.getElementById("chatbot-icon");
    const chatContainer = document.getElementById("chat-container");
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // Estado de la visibilidad del chat (esto es estado de la UI, se queda en el cliente)
    let chatVisible = false;
    // El estado de la conversación (pedido, dirección) ya NO se guarda aquí.

    // Contenedor para quick replies (se inyecta dinámicamente)
    let quickRepliesContainer = null;

    // --- MANEJO DE LA VISIBILIDAD DEL CHAT ---
    chatIcon.addEventListener("click", () => {
        chatVisible = !chatVisible;
        chatContainer.classList.toggle("show", chatVisible);
        if (!chatVisible) {
            clearQuickReplies();
        }
    });

    // --- FUNCIONES AUXILIARES DE LA UI ---

    // Agrega un mensaje al cuadro de chat
    function addMessage(sender, text) {
        const div = document.createElement("div");
        div.classList.add("message");
        // Distingue estilos por emisor
        if (sender === "Tú") {
            div.innerHTML = `<strong>${sender}:</strong> <span class="msg-user">${escapeHtml(text)}</span>`;
            div.style.textAlign = "right";
        } else {
            // Permite saltos de línea en la respuesta del bot
            div.innerHTML = `<strong>${sender}:</strong> <span class="msg-bot">${nl2br(escapeHtml(text))}</span>`;
        }
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
    }

    // Escapa HTML para evitar inyecciones XSS básicas
    function escapeHtml(unsafe) {
        return String(unsafe || "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    // Convierte saltos de línea (\n) a etiquetas <br>
    function nl2br(str) {
        return String(str).replace(/\n/g, "<br>");
    }

    // --- MANEJO DE QUICK REPLIES (BOTONES DE RESPUESTA RÁPIDA) ---

    // Asegura que el contenedor para los botones exista
    function ensureQuickRepliesContainer() {
        if (!quickRepliesContainer) {
            quickRepliesContainer = document.createElement("div");
            quickRepliesContainer.id = "quick-replies";
            quickRepliesContainer.style.display = "flex";
            quickRepliesContainer.style.gap = "8px";
            quickRepliesContainer.style.padding = "8px";
            quickRepliesContainer.style.justifyContent = "center";
            const inputArea = document.querySelector(".chat-input-area");
            inputArea.parentNode.insertBefore(quickRepliesContainer, inputArea);
        }
    }

    // Elimina los botones de respuesta rápida
    function clearQuickReplies() {
        if (quickRepliesContainer) {
            quickRepliesContainer.remove();
            quickRepliesContainer = null;
        }
    }

    // Muestra un conjunto de botones de respuesta rápida
    function showQuickReplies(options = []) {
        ensureQuickRepliesContainer();
        quickRepliesContainer.innerHTML = ""; // Limpiar botones anteriores
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
                // Al hacer clic, se deshabilitan los botones y se envía el mensaje
                Array.from(quickRepliesContainer.children).forEach(b => b.disabled = true);
                addMessage("Tú", opt.value);
                clearQuickReplies();
                await sendMessageToServer(opt.value);
            });
            quickRepliesContainer.appendChild(btn);
        });
    }

    // --- LÓGICA PRINCIPAL DE COMUNICACIÓN ---

    // Función UNIFICADA para enviar mensajes al servidor
    async function sendMessageToServer(messageText) {
        try {
            const resp = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                // El body es ahora muy simple: solo enviamos el mensaje.
                body: JSON.stringify({ mensaje: messageText }),
            });

            if (!resp.ok) throw new Error("Error en la respuesta del servidor: " + resp.status);
            
            const data = await resp.json();

            addMessage("Bot", data.respuesta || "No he podido procesar tu solicitud.");
            
            // El cliente ya no necesita actualizar 'pedido' o 'direccion'.
            // Solo reacciona a la fase que el servidor le indica.
            handleFase(data.fase, data);

        } catch (error) {
            addMessage("Bot", "⚠️ Error de conexión con el servidor. Inténtalo de nuevo.");
            console.error("Error en fetch:", error);
        }
    }

    // Maneja la entrada del usuario (desde el input de texto)
    async function handleUserInput() {
        const mensaje = userInput.value.trim();
        if (!mensaje) return;

        addMessage("Tú", mensaje);
        userInput.value = "";
        clearQuickReplies();
        await sendMessageToServer(mensaje);
    }

    // Reacciona a la fase enviada por el backend para modificar la UI
    function handleFase(fase) {
        switch (fase) {
            case "pago":
                showQuickReplies([
                    { label: "Efectivo", value: "efectivo" },
                    { label: "Tarjeta", value: "tarjeta" },
                    { label: "Transferencia", value: "transferencia" }
                ]);
                break;
            case "final":
            case "inicio":
                // En estas fases, nos aseguramos de que no haya botones de respuesta rápida
                clearQuickReplies();
                break;
            // No se necesita acción para 'direccion' u otras fases por ahora
        }
    }

    // --- EVENT LISTENERS ---
    sendBtn.addEventListener("click", handleUserInput);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            handleUserInput();
        }
    });
});