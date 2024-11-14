const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
);

notificationSocket.onopen = function () {
    console.log('WebSocket открыт');
};

notificationSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);


    if (data.message) {
        const messagesList = document.querySelector('.messages-list');
        const messageItem = document.createElement('li');
        messageItem.className = 'message-item';

        const sendTime = new Date(data.message.send_time); // Получаем дату
        const formattedTime = sendTime.toLocaleString('en-US', {
            month: 'short', // Аббревиатура месяца (например, Nov)
            day: 'numeric', // Число месяца
            year: 'numeric', // Год
            hour: 'numeric', // Часы
            minute: 'numeric', // Минуты
            hour12: true // Формат AM/PM
        });

        messageItem.innerHTML = `
        <a href="#" class="message-link">
            <div class="message-avatar">
                <img src="${data.message.avatar_url}" alt="Avatar" class="avatar-img">
            </div>
            <div class="message-content">
                <span class="message-sender">${data.message.sender}</span>
                <p class="message-text">${data.message.text}</p>
                <span class="message-time">${formattedTime}</span>
            </div>
        </a>
    `;
        messagesList.prepend(messageItem);
    }

    if (data.unread_messages_count !== undefined) {
        const messageBadge = document.querySelector('.notification-badge');
        if (data.unread_messages_count > 0) {
            messageBadge.style.display = 'inline';
        } else {
            messageBadge.style.display = 'none';
        }
    }

    if (data.unread_notifications_count !== undefined) {
        const notificationBadge = document.querySelector('.notification-badge-notifications');
        if (data.unread_notifications_count > 0) {
            notificationBadge.style.display = 'inline';
        } else {
            notificationBadge.style.display = 'none';
        }
    }
};

notificationSocket.onerror = function (error) {
    console.error('Ошибка WebSocket: ', error);
};

notificationSocket.onclose = function (event) {
    console.log('WebSocket закрыт', event);
};
