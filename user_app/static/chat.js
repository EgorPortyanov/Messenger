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

const deleteCover = document.getElementById('deleteCover');
const closeDeleteModalBtn = document.getElementById('closeDeleteModalBtn');
const cancelDeleteModalBtn = document.getElementById('cancelDeleteModalBtn');

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
    
    const activeChatId = localStorage.getItem("active_chat_id");
    
        if (String(data.chat_id) === String(activeChatId)) {
        const newMessage = document.createElement("div");
        newMessage.className = "message-item";
        
        let senderName = data.sender;
        if (senderName === "test@test.com") senderName = "Користувач";
        const now = new Date();
        const timeStr = now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
        const firstLetter = senderName.charAt(0).toUpperCase();
        newMessage.innerHTML = `
            <div class="msg-avatar" style="background: #4DA6FF; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 500;">${firstLetter}</div>
            <div class="msg-content" style="display: flex; flex-direction: column; gap: 4px;">
                <div class="msg-meta" style="display: flex; align-items: center; gap: 8px;">
                    <span class="msg-author" style="font-weight: 600; color: #1A1A1A; font-size: 15px;">${senderName}</span>
                    <span class="msg-time" style="color: #999999; font-size: 12px;">${timeStr}</span>
                </div>
                <div class="msg-text" style="color: #333333; font-size: 15px; line-height: 22px;">${data.text}</div>
            </div>
        `;
        messageContainer.appendChild(newMessage);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

});

socket.on("global_new_message", (data) => {
    console.log("Глобальне сповіщення про повідомлення:", data);
    
    const activeChatId = localStorage.getItem("active_chat_id");
    
    const previewEl = document.querySelector(`[data-chat-preview-id="${data.chat_id}"]`);
    if (previewEl) {
        previewEl.textContent = data.text;
        previewEl.style.fontStyle = "normal";
        previewEl.style.color = "#666666";
    }
    
        const timeEl = document.querySelector(`[data-chat-time-id="${data.chat_id}"]`);
    if (timeEl) {
        timeEl.textContent = "just now";
    }


    if (String(data.chat_id) !== String(activeChatId)) {
        const badge = document.getElementById(`badge-${data.chat_id}`);
        if (badge) {
            let currentCount = parseInt(badge.textContent.trim()) || 0;
            currentCount += 1;
            badge.textContent = currentCount;
            badge.style.display = "flex";
        }
    }
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
                if (senderName === "test@test.com") senderName = "Користувач";
                
                newMessage.innerHTML = `
                    <div class="msg-avatar" style="background: #4DA6FF; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 500;">${msg.avatar_letter}</div>
                    <div class="msg-content" style="display: flex; flex-direction: column; gap: 4px;">
                        <div class="msg-meta" style="display: flex; align-items: center; gap: 8px;">
                            <span class="msg-author" style="font-weight: 600; color: #1A1A1A; font-size: 15px;">${senderName}</span>
                            <span class="msg-time" style="color: #999999; font-size: 12px;">${msg.time}</span>
                        </div>
                        <div class="msg-text" style="color: #333333; font-size: 15px; line-height: 22px;">${msg.text}</div>
                    </div>
                `;
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
    const badge = document.getElementById(`badge-${chatId}`);
    if (badge) {
        badge.textContent = "0";
        badge.style.display = "none";
    }
    await loadUsers(chatId);
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
        
        const chatsPanel = document.getElementById('chatsPanel');
        if (chatsPanel && window.innerWidth <= 768) {
            chatsPanel.classList.remove('open');
        }
    });
}

async function loadUsers(chatId) {
    try {
        let url = '/get_users';
        if (chatId) {
            url += `?chat_id=${chatId}`;
        }
        
        const response = await fetch(url);
        const users = await response.json();
        
        const userList = document.getElementById('userList');
        if (!userList) return;
        
        if (users.length === 0) {
            userList.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Немає користувачів</div>';
            return;
        }
        
        let html = '';
        for (const user of users) {
            const statusClass = user.is_online ? "online-dot" : "offline-dot";
            
            let firstLetter = 'U';
            if (user.first_name && user.first_name.trim() !== '') {
                firstLetter = user.first_name.trim().charAt(0).toUpperCase();
            } else if (user.name && user.name.trim() !== '') {
                firstLetter = user.name.trim().charAt(0).toUpperCase();
            }
            
            const displayUsername = user.username ? (user.username.startsWith('@') ? user.username : '@' + user.username) : `@user${user.id}`;
            
            html += `
                <div class="user-row" data-user-id="${user.id}" data-user-name="${user.name}" data-user-username="${displayUsername}">
                    <div class="user-avatar-sm" style="background:#4DA6FF;">
                        ${firstLetter}
                        <span class="${statusClass}" style="${user.is_online ? 'background: #007AFF;' : 'background: #999999;'}"></span>
                    </div>
                    <span class="user-name">${user.name}</span>
                </div>
            `;
        }
        userList.innerHTML = html;
    } catch (error) {
        console.error("Помилка завантаження користувачів:", error);
    }
}

socket.on("user_status", (data) => {
    console.log("Статус користувача:", data);
    
    const userRow = document.querySelector(`.user-row[data-user-id="${data.user_id}"]`);
    if (userRow) {
        const statusDot = userRow.querySelector(".online-dot, .offline-dot");
        if (statusDot) {
            if (data.status === "online") {
                statusDot.className = "online-dot";
                statusDot.style.background = "#007AFF";
            } else {
                statusDot.className = "offline-dot";
                statusDot.style.background = "#999999";
            }
        }
    }
    
    loadUsers();
});

async function loadUserProfile() {
    try {
        const response = await fetch('/get_users');
        const users = await response.json();
        
        if (users.length > 0) {
            const currentUser = users[0];
            document.getElementById('settingsName').value = currentUser.first_name || '';
            document.getElementById('settingsSurname').value = currentUser.surname || '';
            document.getElementById('settingsUsername').value = currentUser.username || '';
            document.getElementById('settingsGender').value = currentUser.gender || '';
            document.getElementById('settingsBirthDate').value = currentUser.birth_date || '';
            
            updateAvatar(currentUser.first_name, currentUser.surname);
        }
    } catch (error) {
        console.error("Помилка завантаження профілю:", error);
    }
}

function updateAvatar(name, surname) {
    const firstLetter = name ? name.charAt(0).toUpperCase() : '';
    const secondLetter = surname ? surname.charAt(0).toUpperCase() : '';
    const initials = firstLetter + secondLetter || 'AA';

    const settingsAvatar = document.getElementById('settingsAvatar');
    if (settingsAvatar) settingsAvatar.textContent = initials;

    const topbarAvatar = document.querySelector('.topbar-icon-btn.blue-bg span');
    if (topbarAvatar) topbarAvatar.textContent = initials;
}

async function saveSettings() {
    const name = document.getElementById('settingsName').value.trim();
    const surname = document.getElementById('settingsSurname').value.trim();
    const username = document.getElementById('settingsUsername').value.trim();
    const gender = document.getElementById('settingsGender').value;
    const birthDate = document.getElementById('settingsBirthDate').value;
    
    try {
        const response = await fetch('/update_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                surname: surname,
                username: username,
                gender: gender,
                birth_date: birthDate
            })
        });
        
        const data = await response.json();
        if (data.success) {
            updateAvatar(name, surname);
            const settingsCover = document.getElementById('settingsCover');
            if (settingsCover) settingsCover.style.display = 'none';
            const activeChatId = localStorage.getItem("active_chat_id");
            loadUsers(activeChatId);
            alert('Налаштування збережено!');
        } else {
            alert('Помилка сохранения');
        }
    } catch (error) {
        console.error("Помилка:", error);
        alert('Помилка збереження');
    }
}

// Глобальная функция карточки пользователя
async function openUserCard(userId) {
    try {
        console.log("Пытаемся открыть карточку для пользователя с ID:", userId);
        const response = await fetch(`/get_user_profile/${userId}`);
        if (!response.ok) return;
        const user = await response.json();
        
        const profileCover = document.getElementById('profileCover');
        if (!profileCover) return;
        
        let initials = 'U';
        if (user.first_name || user.surname) {
            const f = user.first_name ? user.first_name.trim().charAt(0).toUpperCase() : '';
            const s = user.surname ? user.surname.trim().charAt(0).toUpperCase() : '';
            initials = f + s || 'U';
        }
        
        const avatarElement = document.getElementById('profileAvatar');
        if (avatarElement) {
            avatarElement.innerHTML = `${initials} <span id="profileStatusDot" class="${user.is_online ? 'online-dot' : 'offline-dot'}" style="background: ${user.is_online ? '#007AFF' : '#999999'};"></span>`;
        }
        
        const nameEl = document.getElementById('profileName');
        const usernameEl = document.getElementById('profileUsername');
        const birthDateEl = document.getElementById('profileBirthDate');
        const genderEl = document.getElementById('profileGender');
        
        if (nameEl) nameEl.textContent = user.name || `User ${user.id}`;
        if (usernameEl) {
            const uname = user.username || `user${user.id}`;
            usernameEl.textContent = uname.startsWith('@') ? uname : `@${uname}`;
        }
        if (birthDateEl) birthDateEl.textContent = user.birth_date_text || "Не вказано";
        if (genderEl) genderEl.textContent = user.gender || "Не вказано";
        
        // Показываем карточку как встроенный блок
        profileCover.style.display = 'flex';
    } catch (error) {
        console.error("Глобальная ошибка в функции openUserCard:", error);
    }
}

const settingsBtn = document.getElementById('settingsBtn');
const settingsCover = document.getElementById('settingsCover');
const closeSettingsBtn = document.getElementById('closeSettingsBtn');
const cancelSettingsBtn = document.getElementById('cancelSettingsBtn');
const saveSettingsBtn = document.getElementById('saveSettingsBtn');
const logoutBtn = document.getElementById('logoutBtn');

if (settingsBtn) {
    settingsBtn.addEventListener('click', () => {
        settingsCover.style.display = 'flex';
        loadUserProfile();
    });
}
if (closeSettingsBtn) {
    closeSettingsBtn.addEventListener('click', () => {
        settingsCover.style.display = 'none';
    });
}
if (cancelSettingsBtn) {
    cancelSettingsBtn.addEventListener('click', () => {
        settingsCover.style.display = 'none';
    });
}
if (saveSettingsBtn) {
    saveSettingsBtn.addEventListener('click', saveSettings);
}
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        if (confirm('Ви впевнені, що хочете вийти?')) {
            window.location.href = '/logout';
        }
    });
}
if (settingsCover) {
    settingsCover.addEventListener('click', (event) => {
        if (event.target === settingsCover) {
            settingsCover.style.display = 'none';
        }
    });
}

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

// УДАЛЕНИЕ ЧАТА
const deleteBtn = document.getElementById('deleteChatBtn');
if (deleteBtn) {
    deleteBtn.addEventListener('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        const deleteCover = document.getElementById('deleteCover');
        if (deleteCover) {
            deleteCover.style.display = 'flex';
        } else {
            console.error("Елемент #deleteCover не знайдено!");
        }
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
            messageContainer.innerHTML = 'Виберіть чат для спілкування';
        }
        loadUsers(null);
    }
    
    const profileCover = document.getElementById('profileCover');
    const closeProfileModalBtn = document.getElementById('closeProfileModalBtn');
    
    if (closeProfileModalBtn && profileCover) {
        closeProfileModalBtn.addEventListener('click', () => {
            profileCover.style.display = 'none';
        });
    }
    
    // ❌ УДАЛЕН блок, который закрывал карточку по клику на подложку
    // Теперь карточка закрывается ТОЛЬКО через крестик
    
    const userListContainer = document.getElementById('userList');
    if (userListContainer) {
        userListContainer.addEventListener('click', function(event) {
            const userRow = event.target.closest('.user-row');
            if (userRow) {
                const userId = userRow.getAttribute('data-user-id');
                if (userId) {
                    openUserCard(userId);
                }
            }
        });
    }
    
    loadUserProfile();
    
    const menuToggle = document.getElementById('menuToggle');
    const chatsPanel = document.getElementById('chatsPanel');
    const usersToggle = document.getElementById('usersToggle');
    const usersPanel = document.getElementById('usersPanel');
    const chatsBack = document.getElementById('chatsBack');
    const usersBack = document.getElementById('usersBack');
    
    if (window.innerWidth <= 768) {
        if (menuToggle) menuToggle.style.display = 'flex';
        if (chatsBack) chatsBack.style.display = 'flex';
        if (usersBack) usersBack.style.display = 'flex';
    }
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            if (chatsPanel) chatsPanel.classList.toggle('open');
            if (usersPanel && usersPanel.classList.contains('open')) {
                usersPanel.classList.remove('open');
            }
        });
    }
    
    if (chatsBack) {
        chatsBack.addEventListener('click', function() {
            if (chatsPanel) chatsPanel.classList.remove('open');
        });
    }
    
    if (usersToggle) {
        usersToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            if (usersPanel) usersPanel.classList.toggle('open');
            if (chatsPanel && chatsPanel.classList.contains('open')) {
                chatsPanel.classList.remove('open');
            }
        });
    }
    
    if (usersBack) {
        usersBack.addEventListener('click', function() {
            if (usersPanel) usersPanel.classList.remove('open');
        });
    }
    
    document.addEventListener('click', function(e) {
        const isMobile = window.innerWidth <= 768;
        if (!isMobile) return;
        
        if (chatsPanel && chatsPanel.classList.contains('open')) {
            if (!chatsPanel.contains(e.target) && !menuToggle.contains(e.target)) {
                chatsPanel.classList.remove('open');
            }
        }
        if (usersPanel && usersPanel.classList.contains('open')) {
            if (!usersPanel.contains(e.target) && !usersToggle.contains(e.target)) {
                usersPanel.classList.remove('open');
            }
        }
    });
    
    window.addEventListener('resize', function() {
        if (window.innerWidth <= 768) {
            if (menuToggle) menuToggle.style.display = 'flex';
            if (chatsBack) chatsBack.style.display = 'flex';
            if (usersBack) usersBack.style.display = 'flex';
        } else {
            if (menuToggle) menuToggle.style.display = 'none';
            if (chatsBack) chatsBack.style.display = 'none';
            if (usersBack) usersBack.style.display = 'none';
            if (chatsPanel) chatsPanel.classList.remove('open');
            if (usersPanel) usersPanel.classList.remove('open');
        }
    });
});