const notificationSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/notifications/'
);

notificationSocket.onopen = function () {
    console.log('WebSocket открыт');
};

notificationSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const unreadMessagesCount = data.unread_messages_count;
    const badge = document.querySelector('.notification-badge');

    if (unreadMessagesCount > 0) {
        badge.style.display = 'inline';
    } else {
        badge.style.display = 'none';
    }
};

notificationSocket.onerror = function (error) {
    console.error('Ошибка WebSocket: ', error);
};

notificationSocket.onclose = function (event) {
    console.log('WebSocket закрыт', event);
};
