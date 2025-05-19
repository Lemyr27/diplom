document.addEventListener('DOMContentLoaded', async () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const openKeywordsButton = document.getElementById('open-keywords-button');
    const chatMessages = document.getElementById('chat-messages');
    const chatKeywords = document.getElementById('chat-keywords');
    const downloadButton = document.getElementById('download-button'); // Получаем SVG
    const downloadModal = document.getElementById('download-modal'); // Получаем модальное окно
    const closeButton = document.querySelector('.close-button'); // Получаем кнопку закрытия

    let response = await fetch('/chat', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    });
    data = await response.json()

    let msg;
    let url;
    for (let i = 0; i < data.messages.length; i++) {
        msg = data.messages[i];
        displayMessage(msg.user_msg, 'user');
        url = `<br><br>Источник: <a style="text-decoration: none;" href="${msg.url}" target="_blank">${msg.filename}</a>`;
        displayMessage(msg.bot_msg + url, 'bot');
    }

    for (let i = 0; i < data.keywords.length; i++) {
        displayKeyword(data.keywords[i]);
    }

    sendButton.addEventListener('click', async () => {
        const messageText = messageInput.value.trim();
        if (messageText !== '') {
            displayMessage(messageText, 'user');
            messageInput.value = '';

            try {
                let message = {
                    content: messageText
                }
                response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(message)
                });

                if (response.ok) {
                    data = await response.json();
                    url = `<br><br>Источник: <a style="text-decoration: none;" href="${data.url}" target="_blank">${data.filename}</a>`;
                    displayMessage(data.text + url, 'bot');
                } else {
                    displayMessage('Ошибка: к сожалению, мы не нашли ответ на ваш вопрос.', 'bot');
                }
            } catch (error) {
                displayMessage('Error: ' + error, 'bot');
            }
        }
    });

    openKeywordsButton.addEventListener('click', async () => {
        if (chatKeywords.style.display === "none") {
            chatKeywords.style.display = "flex";
        } else {
            chatKeywords.style.display = "none"
        };
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    chatMessages.scrollTop = chatMessages.scrollHeight;

    function displayMessage(message, sender) {
        const messageElement = document.createElement('p');
        messageElement.classList.add(sender + '-message');
        messageElement.innerHTML = message;
        chatMessages.appendChild(messageElement);

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function displayKeyword(keyword) {
        const keywordElement = document.createElement('p');
        keywordElement.classList.add('keyword');
        keywordElement.innerHTML = keyword;
        chatKeywords.appendChild(keywordElement);
    }

    // Обработчики событий для модального окна
    downloadButton.addEventListener('click', () => {
        downloadModal.style.display = "block";
    });

    closeButton.addEventListener('click', () => {
        downloadModal.style.display = "none";
    });

    window.addEventListener('click', (event) => {
        if (event.target == downloadModal) {
            downloadModal.style.display = "none";
        }
    });
});