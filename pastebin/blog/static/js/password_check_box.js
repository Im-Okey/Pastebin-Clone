document.addEventListener('DOMContentLoaded', function () {
    var checkbox = document.getElementById('need-password');
    var passwordField = document.getElementById('password-field');

    // Функция для переключения состояния поля пароля
    function togglePasswordField() {
        if (checkbox.checked) {
            passwordField.disabled = false; // Разблокировать поле пароля
            passwordField.value = '';       // Очистить поле для нового пароля
        } else {
            passwordField.disabled = true;  // Заблокировать поле пароля
            passwordField.value = '';       // Очистить поле
        }
    }

    // Проверка начального состояния при загрузке страницы
    passwordField.disabled = true; // Начально заблокировано

    // Слушатель для изменения состояния чекбокса
    checkbox.addEventListener('change', togglePasswordField);
});