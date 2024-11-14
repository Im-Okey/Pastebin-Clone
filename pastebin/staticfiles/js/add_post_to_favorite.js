function toggleFavorite(element) {
    const star = element.querySelector('.star');
    const postSlug = element.getAttribute('data-post-slug');

    const toggleFavoriteUrl = `/users/toggle-favorite/${postSlug}/`;

    fetch(toggleFavoriteUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.is_favorite) {
                star.innerHTML = '★';
                star.style.color = '#FFD700';
            } else {
                star.innerHTML = '☆';
                star.style.color = 'black';
            }
        })
        .catch(error => console.error('Ошибка:', error));
}

document.querySelectorAll('.post-favorite').forEach(item => {
    item.addEventListener('click', function () {
        toggleFavorite(this);
    });
});
