document.addEventListener("DOMContentLoaded", function () {
    // Функция для отображения формы редактирования
    function showEditForm(button) {
        console.log("Кнопка редактирования нажата");

        // Скрываем текущий контент поста
        document.getElementById('post-content-display').style.display = 'none';

        // Показываем форму редактирования
        document.getElementById('edit-post-form').style.display = 'block';

        // Прячем кнопку редактирования
        button.style.display = 'none';

        console.log("Форма редактирования теперь видна");

        // Инициализируем редактор после того, как форма будет видна
        initializeEditor();
    }

    // Функция для инициализации CodeMirror
    function initializeEditor() {
        console.log("Инициализация редактора...");

        // Убедимся, что форма полностью загружена
        setTimeout(function() {
            var textarea = document.querySelector(".post-editor1 textarea");  // Скрытое textarea
            if (!textarea) {
                console.error("Textarea не найдено!");
                return;
            }

            console.log("Textarea найдено, значение: ", textarea.value);  // Логируем текущее значение в textarea

            var languageSelect = document.getElementById("language-select");

            // Инициализация CodeMirror
            var editor = CodeMirror.fromTextArea(textarea, {
                mode: languageSelect.value || "plaintext",  // Устанавливаем начальный язык
                lineNumbers: true,
                theme: "base16-light",
                indentUnit: 4,
                autoCloseBrackets: true,  // Включаем автозакрытие скобок
                matchBrackets: true  // Подсветка скобок
            });

            // Загружаем текст в редактор, только если он не пустой
            editor.setValue(textarea.value);

            setTimeout(function () {
                editor.refresh();  // Обновляем редактор, чтобы он правильно отображался
                console.log("Editor refreshed");
            }, 100);

            // Слушаем изменение языка и обновляем подсветку
            languageSelect.addEventListener("change", function () {
                var mode = this.value;
                console.log("Изменен язык: ", mode);
                editor.setOption("mode", mode === "plaintext" ? null : mode);
            });

            // Синхронизация скрытого textarea с редактором при отправке формы
            document.querySelector("form").addEventListener("submit", function (event) {
                var content = editor.getValue();
                console.log("Содержимое редактора перед отправкой: ", content);
                if (!content.trim()) {
                    event.preventDefault();  // Если пусто, не отправляем
                    alert('Поле не может быть пустым!');
                    return false;
                }
                textarea.value = content;  // Переносим значение обратно в textarea
                console.log("Содержимое редактора записано в textarea");
            });
        }, 500); // Небольшая задержка, чтобы форма успела отобразиться
    }

    // Если кнопка для редактирования присутствует, добавляем слушатель события
    var editButton = document.getElementById("edit-button");
    if (editButton) {
        console.log("Кнопка редактирования найдена");
        editButton.addEventListener("click", function () {
            showEditForm(this);  // Показываем форму редактирования
        });
    } else {
        console.error("Кнопка редактирования не найдена!");
    }
});