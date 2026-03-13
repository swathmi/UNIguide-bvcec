// ===============================
// GLOBAL VARIABLES
// ===============================
let currentChatId = null;

// ===============================
// MODAL FUNCTIONS
// ===============================
function openProfileModal() {
    document.getElementById("profileModal").style.display = "flex";
}

function closeProfileModal() {
    document.getElementById("profileModal").style.display = "none";
}

// ===============================
// Send Suggestion Function
// ===============================
function sendSuggestion(text) {
    document.getElementById("userInput").value = text;
    sendMessage();
}
// ===============================
// Typing / Thinking Indicator
// ===============================
function addThinkingMessage() {
    const chatBody = document.getElementById("chat-body");

    const msg = document.createElement("div");
    msg.className = "thinking-msg";


    msg.innerHTML = `
        <i>UNIGuide is thinking</i>
        <span class="dots">
            <span>.</span><span>.</span><span>.</span>
        </span>
        `;


    chatBody.appendChild(msg);
    chatBody.scrollTop = chatBody.scrollHeight;
    return msg;
}


// ===============================
// ===============================
// Send Message Function
// ===============================
function sendMessage() {
    let input = document.getElementById("userInput");
    let text = input.value.trim();
    if (!text) return;
    if (!currentChatId) {
        alert("Please create a new chat first.");
        return;
    }

    addMessage(text, "user");
    input.value = "";

    let thinkingDiv = addThinkingMessage();

    fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            message: text,
            session_id: currentChatId
        })
    })
    .then(res => res.json())
    .then(data => {
        thinkingDiv.remove();

        if (typeof data.answer === "object") {
            addMessage(data.answer, "bot");
        } else {
            addMessage(data.answer, "bot", false);
        }
    })
    .catch(() => {
        thinkingDiv.remove();
        addMessage("⚠️ Server error!", "bot");
    });
}

// Send Message Function
// ===============================
function addMessage(content, type, stream = false) {
    const chatBody = document.getElementById("chat-body");
    const messageDiv = document.createElement("div");

    messageDiv.className =
        "message " + (type === "user" ? "user-message" : "bot-message");

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";

    // PROFILE CARD
    if (typeof content === "object" && content.type === "profile_with_text") {
        contentDiv.innerHTML = `
          <div class="profile-card">
            <img src="${content.photo}" class="profile-img">
            <div>
              <h4>${content.name}</h4>
              <b>${content.designation}</b>
              <p>${content.description}</p>
            </div>
          </div>
        `;
    }
    // TEXT + IMAGES
    else if (typeof content === "object" && content.type === "text_with_images") {
        contentDiv.innerHTML = `
          <h4>${content.emoji} ${content.title}</h4>
          <p>${content.text}</p>
          <div class="image-gallery">
            ${content.images.map(img =>
              `<img src="${img.url}" class="gallery-img">`
            ).join("")}
          </div>
        `;
    }
    // NORMAL TEXT
    else {
        // If backend already sends HTML (iframe, div, etc.)
        if (/<[a-z][\s\S]*>/i.test(content)) {
    contentDiv.innerHTML = content;

        } else {
            // Split by multiple line breaks and paragraphs
            let paragraphs = content
                .split(/\n\s*\n/)  // Split on double newlines (paragraph breaks)
                .filter(p => p.trim().length > 0);
            
            let htmlContent = '';
            
            for (let paragraph of paragraphs) {
                // Split paragraph into lines
                let lines = paragraph.split('\n').filter(line => line.trim().length > 0);
                
                for (let line of lines) {
                    let processedLine = line.trim();
                    
                    // Handle markdown links [text](url)
                    processedLine = processedLine.replace(/\[([^\]]+)\]\(([^)]+\.pdf)\)/g, 
                        '<a href="$2" target="_blank" class="pdf-link">📄 $1</a>');
                    processedLine = processedLine.replace(/\[([^\]]+)\]\(([^)]+)\)/g, 
                        '<a href="$2" target="_blank">$1</a>');
                    
                    // Check if line has emoji prefix (title or bullet)
                    const hasEmojiPrefix = processedLine.match(/^[🔹💼📖🧪📣🎖️📚🚀💡🎯🏆🎉🏢📊🎓📌🚗🎯🏭👥🧑🎯💼🚀🌟📝🏅📂🎉🏢💻🧮🗣️💬📋✔️🔹📖🔧📐]/);

                    
                    if (hasEmojiPrefix || processedLine.includes(':')) {
                        // Likely a title or section header
                        htmlContent += `<div style="margin: 8px 0 4px 0; font-weight: 500;">${processedLine}</div>`;
                    } else if (processedLine.startsWith('•') || processedLine.startsWith('-')) {
                        // Bullet point
                        htmlContent += `<div style="margin-left: 20px; margin: 3px 0 3px 20px;">${processedLine}</div>`;
                    } else if (processedLine.match(/^\d+\./)) {
                        // Numbered list
                        htmlContent += `<div style="margin-left: 20px; margin: 3px 0 3px 20px;">${processedLine}</div>`;
                    } else {
                        // Regular text
                        htmlContent += `<div style="margin: 4px 0;">${processedLine}</div>`;
                    }
                }
            }
            
            if (stream) {
                streamText(htmlContent, contentDiv);
            } else {
                contentDiv.innerHTML = htmlContent;
            }
        }
    }

    // Timestamp
    if (type !== "user") {
        const meta = document.createElement("div");
        meta.className = "message-meta";
        meta.innerHTML = `
          <span class="time">
            ${new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}
          </span>
          <span class="action">👍</span>
          <span class="action">👎</span>
        `;
        messageDiv.appendChild(meta);
    }

    messageDiv.appendChild(contentDiv);
    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// ===============================
// Enter Key Support
// ===============================


// ===============================
// Open/Close Chat
// ===============================


// ===============================
// Scroll Reveal (for landing page)
// ===============================
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
function openPreview(url) {
  const modal = document.getElementById("previewModal");
  const frame = document.getElementById("previewFrame");

  frame.src = url;
  modal.style.display = "flex";
}

function closePreview() {
  const modal = document.getElementById("previewModal");
  const frame = document.getElementById("previewFrame");

  frame.src = "";
  modal.style.display = "none";
}
// ===============================
// Streaming Text Effect
// ===============================
function streamText(text, element, speed = 15) {
    let i = 0;
    element.innerHTML = "";

    const interval = setInterval(() => {
        if (i < text.length) {
            element.innerHTML += text[i];
            i++;
        } else {
            clearInterval(interval);
        }
    }, speed);
}


function startVoice() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-IN";
  recognition.start();

  recognition.onresult = function(e) {
    document.getElementById("userInput").value =
      e.results[0][0].transcript;
    sendMessage();
  };
}

document.addEventListener("DOMContentLoaded", function () {

  // load previous chat
  loadSessions();


  // enter key support
  let input = document.getElementById("userInput");
  if (input) {
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        sendMessage();
      }
    });
  }

});
// ===============================
// CHAT SESSIONS (Sidebar Logic)
// ===============================

function createNewChat() {
  fetch("/api/new_chat", { method: "POST" })
    .then(res => res.json())
    .then(data => {
      currentChatId = data.session_id;
      document.getElementById("chat-body").innerHTML = "";
      loadSessions();
    });
}
function loadSessions() {
  fetch("/api/sessions")
    .then(res => res.json())
    .then(data => {
      const chatList = document.getElementById("chatList");
      chatList.innerHTML = "";

      data.forEach(session => {
        const div = document.createElement("div");
        div.className = "chat-item";

        div.innerHTML = `
          <span onclick="openSession(${session.id})">
              ${session.title}
          </span>

          <span onclick="renameChat(${session.id})"
                style="margin-left:5px;cursor:pointer;">
              ✏️
          </span>

          <span onclick="deleteChat(${session.id})"
                style="float:right;cursor:pointer;">
              🗑
          </span>
        `;

        chatList.appendChild(div);
      });
    });
}
function deleteChat(id) {
    fetch(`/api/delete_session/${id}`, {
        method: "DELETE"
    })
    .then(() => {
        loadSessions();
        document.getElementById("chat-body").innerHTML = "";
    });
}
function renameChat(id) {
    const newTitle = prompt("Enter new chat title:");

    if (!newTitle) return;

    fetch(`/api/rename_session/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle })
    })
    .then(() => loadSessions());
}

function openSession(id) {
  currentChatId = id;
  document.querySelectorAll(".chat-item").forEach(el => {
      el.classList.remove("active");
  });

  // 🔥 Add active to clicked one
  const clickedItem = Array.from(document.querySelectorAll(".chat-item"))
      .find(item => item.innerText.includes(id)); // fallback safe

  if (event && event.target) {
      event.target.closest(".chat-item")?.classList.add("active");
  }

  fetch(`/api/session/${id}`)
    .then(res => res.json())
    .then(messages => {
      const chatBody = document.getElementById("chat-body");
      chatBody.innerHTML = "";

      messages.forEach(m => {
        addMessage(m.message, "user");
        addMessage(m.response, "bot");
      });
    });
}
function searchChats() {
    const input = document.getElementById("searchChat").value.toLowerCase();
    const items = document.querySelectorAll("#chatList .chat-item");

    items.forEach(item => {
        const text = item.querySelector("span").innerText.toLowerCase();

        if (text.includes(input)) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    });
}



// ===============================
// Advanced Profile System
// ===============================
document.addEventListener("DOMContentLoaded", function () {

    const circle = document.getElementById("profileCircle");
    const profile = document.querySelector(".profile-dropdown");
    const dropdown = profile ? profile.querySelector(".dropdown-menu") : null;
     if (!circle || !profile || !dropdown) return;

    // Random Stable Color
    function stringToColor(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = str.charCodeAt(i) + ((hash << 5) - hash);
        }
        return `hsl(${Math.abs(hash) % 360}, 70%, 50%)`;
    }

    if (!circle.querySelector("img")) {
        const name = circle.textContent.trim();
        const bg = stringToColor(name);
        circle.style.backgroundColor = bg;
        circle.style.color = "#fff";
    }

    // Click dropdown
    profile.addEventListener("click", function (e) {
        dropdown.classList.toggle("active");
        e.stopPropagation();
    });

    document.addEventListener("click", function () {
        dropdown.classList.remove("active");
    });

});

document.addEventListener("DOMContentLoaded", function () {

    const circle = document.getElementById("profileCircle");
    const dropdown = document.getElementById("dropdownMenu");

    if (!circle || !dropdown) return;

    circle.addEventListener("click", function (e) {
        dropdown.classList.toggle("active");
        e.stopPropagation();
    });

    document.addEventListener("click", function () {
        dropdown.classList.remove("active");
    });

});








