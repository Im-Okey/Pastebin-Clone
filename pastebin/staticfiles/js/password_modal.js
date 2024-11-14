document.addEventListener('DOMContentLoaded', function () {
    function goBack() {
        window.history.back();
    }

    const postPasswordElement = document.getElementById('post-password');

    if (postPasswordElement) {
        const postPassword = postPasswordElement.value;

        if (postPassword) {
            document.getElementById('post-content').classList.add('blurred');

            document.getElementById('passwordModal').style.display = 'flex';

            document.body.classList.add('blocked');
            document.body.style.overflow = 'hidden';
        }
    }
});