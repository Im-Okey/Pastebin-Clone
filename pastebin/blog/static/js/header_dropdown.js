document.addEventListener('DOMContentLoaded', function () {
    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown');

    dropdownToggle.addEventListener('click', function () {
        dropdownMenu.classList.toggle('show');
    });

    window.addEventListener('click', function (event) {
        if (!dropdownToggle.contains(event.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
});
