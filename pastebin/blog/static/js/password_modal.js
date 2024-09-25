document.addEventListener('DOMContentLoaded', function () {
    // Функция возврата на предыдущую страницу
    function goBack() {
        window.history.back();
    }

    // Проверяем наличие элемента с ID 'post-password'
    const postPasswordElement = document.getElementById('post-password');

    // Если элемент существует, проверяем его значение
    if (postPasswordElement) {
        const postPassword = postPasswordElement.value; // Получаем значение пароля

        // Если требуется пароль, применяем размытие к контенту и показываем модальное окно
        if (postPassword) {
            document.getElementById('post-content').classList.add('blurred'); // Применяем размытие к контенту

            // Показываем модальное окно
            document.getElementById('passwordModal').style.display = 'flex'; // Убедитесь, что модальное окно отображается

            // Блокируем прокрутку страницы
            document.body.classList.add('blocked'); // Блокируем прокрутку страницы
            document.body.style.overflow = 'hidden'; // Запрещаем прокрутку
        }
    }
});