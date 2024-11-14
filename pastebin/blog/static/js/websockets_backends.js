const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
);

notificationSocket.onopen = function () {
    console.log('WebSocket открыт');
};

notificationSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);

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
