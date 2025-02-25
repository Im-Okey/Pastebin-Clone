setTimeout(function () {
    const messages = document.querySelector('#messages');
    if (messages) {
        messages.style.opacity = 0;
        setTimeout(() => {
            messages.style.display = 'none';
        }, 500);
    }
}, 5000);
