// ===============================
// Send Message Function
// ===============================
function sendMessage() {
    let input = document.getElementById("userInput");
    let text = input.value.trim();

    if (!text) return;

    // Add user message
    addMessage(text, "user");
    input.value = "";

    // Show typing indicator
    let typingDiv = addTypingIndicator();

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: text })
    })
    .then(res => res.json())
    .then(data => {
        typingDiv.remove();

        console.log("BOT RESPONSE:", data);

        // Add bot response
        addMessage(data.answer, "bot");
    })
    .catch(() => {
        typingDiv.remove();
        addMessage("⚠ Server not responding! Please try again.", "bot");
    });
}

// ===============================
// Typing Indicator
// ===============================
function addTypingIndicator() {
    let chatBody = document.getElementById("chat-body");
    let messageDiv = document.createElement("div");

    messageDiv.classList.add("message", "bot-message");
    messageDiv.innerHTML = `
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;

    return messageDiv;
}

// ===============================
// Add Message to Chat
// ===============================
function addMessage(content, type) {
    let chatBody = document.getElementById("chat-body");
    let messageDiv = document.createElement("div");

    messageDiv.classList.add(
        "message",
        type === "user" ? "user-message" : "bot-message"
    );

    // PROFILE CARD RESPONSE
    if (
        type === "bot" &&
        typeof content === "object" &&
        content.type === "profile_with_text"
    ) {
        messageDiv.innerHTML = `
            <div class="management-block">
                <h4 class="mgmt-name">${content.name}</h4>
                <p class="mgmt-desc">${content.description}</p>

                <div class="profile-card">
                    <img src="${content.photo}" alt="${content.name}">
                    <p class="mgmt-designation">${content.designation}</p>
                </div>
            </div>
        `;
    }
    // NORMAL TEXT RESPONSE
    else {
        messageDiv.textContent = content;
    }

    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// ===============================
// Enter Key Support
// ===============================
document
    .getElementById("userInput")
    .addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            sendMessage();
        }
    });


// =================================================
// 🔥 NEW ADDITIONS (LANDING → CHAT FLOW)
// =================================================

// Open chatbot from landing page
function openChat() {
    const landing = document.getElementById("landing");
    const chatbot = document.getElementById("chatbotContainer");

    if (landing) landing.style.display = "none";
    if (chatbot) chatbot.style.display = "flex";

    // Auto focus input
    setTimeout(() => {
        document.getElementById("userInput")?.focus();
    }, 300);
}

// Open chatbot with predefined question (future use)
function openChatWithText(text) {
    openChat();
    document.getElementById("userInput").value = text;
}
// =====================================================
// Scroll Reveal Animation
// =====================================================
const reveals = document.querySelectorAll(".reveal");

window.addEventListener("scroll", () => {
    reveals.forEach(el => {
        const windowHeight = window.innerHeight;
        const elementTop = el.getBoundingClientRect().top;

        if (elementTop < windowHeight - 100) {
            el.classList.add("active");
        }
    });
});


