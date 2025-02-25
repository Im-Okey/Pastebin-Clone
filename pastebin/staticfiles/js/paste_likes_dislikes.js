function likeDislikePaste(pasteId, action) {
    const likeButton = document.querySelector(`#like-button-${pasteId}`);
    const dislikeButton = document.querySelector(`#dislike-button-${pasteId}`);
    const likeCount = document.querySelector(`#like-count-${pasteId}`);
    const dislikeCount = document.querySelector(`#dislike-count-${pasteId}`);

    let url = '';

    if (action === 'like') {
        url = `/general/like/${pasteId}/`;
    } else if (action === 'dislike') {
        url = `/general/dislike/${pasteId}/`;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        likeCount.textContent = data.likes_count;
        dislikeCount.textContent = data.dislikes_count;

        if (data.liked) {
            likeButton.style.color = 'blue';
            dislikeButton.style.color = 'black';
        } else if (data.disliked) {
            dislikeButton.style.color = 'red';
            likeButton.style.color = 'black';
        } else {
            likeButton.style.color = 'black';
            dislikeButton.style.color = 'black';
        }
    })
    .catch(error => console.error('Ошибка:', error));
}

function getCsrfToken() {
    let csrfToken = null;
    const cookies = document.cookie.split(';');
    cookies.forEach(cookie => {
        const [name, value] = cookie.split('=');
        if (name.trim() === 'csrftoken') {
            csrfToken = value;
        }
    });
    return csrfToken;
}