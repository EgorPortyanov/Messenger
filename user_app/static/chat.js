const socket = io();

const sendBtn = document.querySelector("#sendBtn");
const messageInput = document.querySelector("#messageInput");
const messageContainer = document.querySelector("#realMessages");

const openBtn = document.getElementById('openModalBtn');
const closeBtn = document.getElementById('closeModalBtn');
const cancelBtn = document.getElementById('cancelModalBtn');
const cover = document.getElementById('cover');

if (openBtn) {
    openBtn.addEventListener('click', () => {
        cover.style.display = 'flex';
    });
}

if (closeBtn) {
    closeBtn.addEventListener('click', () => {
        cover.style.display = 'none';
    });
}

if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
        cover.style.display = 'none';
    });
}

if (cover) {
    cover.addEventListener('click', (event) => {
        if (event.target === cover) {
            cover.style.display = 'none';
        }
    });
}

const deleteBtn = document.querySelector('.icon-btn');
const deleteCover = document.getElementById('deleteCover');
const closeDeleteModalBtn = document.getElementById('closeDeleteModalBtn');
const cancelDeleteModalBtn = document.getElementById('cancelDeleteModalBtn');

if (deleteBtn) {
    deleteBtn.addEventListener('click', (event) => {
        event.preventDefault();
        deleteCover.style.display = 'flex';
    });
}

if (closeDeleteModalBtn) {
    closeDeleteModalBtn.addEventListener('click', () => {
        deleteCover.style.display = 'none';
    });
}

if (cancelDeleteModalBtn) {
    cancelDeleteModalBtn.addEventListener('click', () => {
        deleteCover.style.display = 'none';
    });
}

if (deleteCover) {
    deleteCover.addEventListener('click', (event) => {
        if (event.target === deleteCover) {
            deleteCover.style.display = 'none';
        }
    });
}

function sendMessage() {
    const message = messageInput.value;
    if (message === null || message.trim() === "") return;
    
    const activeChat = document.querySelector(".chat-window-header h3");
    const activeChatId = localStorage.getItem("active_chat_id");
    
    if (!activeChatId) return;

    socket.emit("send", {
        "text": message,
        "chat_id": activeChatId
    });
    messageInput.value = "";
}



if (sendBtn) {
    sendBtn.addEventListener("click", sendMessage);
}

socket.on("receive_message", (data) => {
    console.log("Отримано повідомлення:", data);
    
    const newMessage = document.createElement("div");
    newMessage.className = "message-item";
    let senderName = data.sender;
    if (senderName === "test@test.com") {
        senderName = "Користувач";
    }
    newMessage.innerHTML = `<div class="msg-text"><strong>${senderName}:</strong> ${data.text}</div>`;
    messageContainer.appendChild(newMessage);
    messageContainer.scrollTop = messageContainer.scrollHeight;
});

async function loadChat(chatId, chatName) {
    if (!chatId) return;

    const chatHeader = document.querySelector(".chat-window-header h3");
    if (chatHeader && chatName) chatHeader.textContent = chatName;
    
    socket.emit("connect_chat", chatId);
    
    if (messageContainer) {
        messageContainer.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Завантаження...</div>';
    }
    
    try {
        const response = await fetch(`/get_messages/?chat_id=${chatId}`);
        const messages = await response.json();
        
        if (!messageContainer) return;
        
        if (messages.length === 0) {
            messageContainer.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Виберіть чат для спілкування</div>';
        } else {
            messageContainer.innerHTML = '';
            for (const msg of messages) {
                const newMessage = document.createElement("div");
                newMessage.className = "message-item";
                let senderName = msg.sender;
                if (senderName === "test@test.com") {
                    senderName = "Користувач";
                }
                newMessage.innerHTML = `<div class="msg-text"><strong>${senderName}:</strong> ${msg.text}</div>`;
                messageContainer.appendChild(newMessage);
            }
            messageContainer.scrollTop = messageContainer.scrollHeight;
        }
    } catch (error) {
        console.error("Ошибка загрузки сообщений:", error);
        if (messageContainer) {
            messageContainer.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Помилка завантаження</div>';
        }
    }
}

const chatRows = document.querySelectorAll(".chat-row");
for (const chatRow of chatRows) {
    chatRow.addEventListener("click", function() {
        const chatId = this.getAttribute("data-chat-id");
        if (!chatId) return;
        
        const chatName = this.querySelector(".chat-name").textContent;
        console.log(`Клікнули на чат: ID=${chatId}, NAME=${chatName}`);
        
        localStorage.setItem("active_chat_id", chatId);
        localStorage.setItem("active_chat_name", chatName);
        
        loadChat(chatId, chatName);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const savedChatId = localStorage.getItem("active_chat_id");
    const savedChatName = localStorage.getItem("active_chat_name");

    if (savedChatId) {
        console.log(`Автоматично відновлюємо чат ID=${savedChatId} на новій вкладці`);
        loadChat(savedChatId, savedChatName);
    } else {
        if (messageContainer) {
            messageContainer.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Виберіть чат для спілкування</div>';
        }
    }
});

if (messageInput) {
    messageInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
}

const deleteForm = document.getElementById('deleteForm');

if (deleteForm) {
    deleteForm.addEventListener('submit', () => {
        
        localStorage.removeItem("active_chat_id");
        localStorage.removeItem("active_chat_name");
    });
}
