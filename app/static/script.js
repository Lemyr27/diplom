document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');

    sendButton.addEventListener('click', async () => {
        const messageText = messageInput.value.trim();
        if (messageText !== '') {
            displayMessage(messageText, 'user');
            messageInput.value = '';

            try {
                const response = await fetch('/search?q=' + messageText, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    const url = `<br><br>Источник: <a style="text-decoration: none;" href="${data.url}" target="_blank">${data.filename}</a>`;
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