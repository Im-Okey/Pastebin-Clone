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

        const sendTime = new Date(data.message.send_time);
        const formattedTime = sendTime.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            hour12: true
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
                ${!data.message.is_checked ? `<span class="notification-badge"></span>` : ''}
            </a>
        `;
        messagesList.prepend(messageItem);
    }


    if (data.notification) {

        const notificationsList = document.querySelector('.notifications-list');
        const notificationItem = document.createElement('li');
        notificationItem.className = 'notification-item';

        const sendTime = new Date(data.notification.send_time);
        const formattedTime = sendTime.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            hour12: true
        });

        notificationItem.innerHTML = `
            <a href="${data.notification.url}" class="notification-link">
                <div class="notification-avatar">
                    <img src="${data.notification.avatar_url}" alt="Avatar" class="avatar-img">
                </div>
                <div class="notification-content">
                    <p class="notification-message">${data.notification.message}</p>
                    <span class="notification-time">${formattedTime}</span>
                </div>
                ${data.notification.is_checked ? '' : '<span class="notification-badge"></span>'}
            </a>
        `;

        notificationsList.prepend(notificationItem);
    }

    if (data.unread_messages_count !== undefined) {

        const messageCount = document.querySelector('.card-title .unread-count');
        if (messageCount) {
            messageCount.textContent = `(${data.unread_messages_count})`;
        }

        const messageBadge = document.querySelector('.notification-badge');
        if (data.unread_messages_count > 0) {
            messageBadge.style.display = 'inline';
        } else {
            messageBadge.style.display = 'none';
        }
    }


    if (data.unread_notifications_count !== undefined) {
        const notificationTitle = document.querySelector('.card-title');

        if (notificationTitle) {
            // Убираем старый текст и вставляем новый счетчик
            notificationTitle.innerHTML = `Уведомления (${data.unread_notifications_count})`;
        }

        const notificationBadge = document.querySelector('.notification-badge-notifications');
        if (notificationBadge) {
            notificationBadge.style.display = data.unread_notifications_count > 0 ? 'inline' : 'none';
        }
    }
};

notificationSocket.onerror = function (error) {
    console.error('Ошибка WebSocket: ', error);
};

notificationSocket.onclose = function (event) {
    console.log('WebSocket закрыт', event);
};
