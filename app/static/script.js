document.addEventListener('DOMContentLoaded', async () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');


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

    function displayMessage(message, sender) {
        const messageElement = document.createElement('p');
        messageElement.classList.add(sender + '-message');
        messageElement.innerHTML = message;
        chatMessages.appendChild(messageElement);

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});