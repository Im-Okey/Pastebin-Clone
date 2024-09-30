document.addEventListener('DOMContentLoaded', function () {
    var checkbox = document.getElementById('need-password');
    var passwordField = document.getElementById('password-field');
    var storedPasswordField = document.getElementById('stored-password');

    // Функция для переключения состояния поля пароля
    function togglePasswordField() {
        if (checkbox.checked) {
            passwordField.disabled = false; // Разблокировать поле пароля
            passwordField.value = '';       // Очистить поле для нового пароля
        } else {
            passwordField.disabled = true;  // Заблокировать поле пароля
            // Если поле пароля заблокировано, берем хеш пароля из скрытого поля
            passwordField.value = '';       // Очистить поле
        }
    }

    // Проверка начального состояния при загрузке страницы
    passwordField.disabled = true; // Начально заблокировано

    // Установка значения скрытого поля при загрузке страницы
    if (passwordField.value) {
        storedPasswordField.value = passwordField.value; // Устанавливаем хеш пароля в скрытое поле
    }

    // Слушатель для изменения состояния чекбокса
    checkbox.addEventListener('change', togglePasswordField);
});