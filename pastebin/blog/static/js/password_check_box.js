document.addEventListener('DOMContentLoaded', function () {
    var passwordFieldId = document.querySelector('[data-password-id]').getAttribute('data-password-id');
    var passwordField = document.getElementById(passwordFieldId);
    var checkbox = document.getElementById('need-password');

    function togglePasswordField() {
        if (checkbox.checked) {
            passwordField.disabled = false;
        } else {
            passwordField.disabled = true;
            passwordField.value = '';
        }
    }

    passwordField.disabled = true;

    checkbox.addEventListener('click', togglePasswordField);
});