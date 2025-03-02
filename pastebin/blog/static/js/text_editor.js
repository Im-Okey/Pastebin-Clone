document.addEventListener("DOMContentLoaded", function () {
    var textarea = document.querySelector(".post-editor1 textarea");
    var languageSelect = document.getElementById("language-select");
    console.log("Форма редактирования теперь видна");
    var editor = CodeMirror.fromTextArea(textarea, {
        mode: languageSelect.value || "plaintext",
        lineNumbers: true,
        theme: "base16-light",
        indentUnit: 4
    });

    editor.setValue(textarea.value);

    setTimeout(() => {
        editor.refresh();
    }, 100);

    languageSelect.addEventListener("change", function () {
        var mode = this.value;
        editor.setOption("mode", mode === "plaintext" ? null : mode);
    });

    document.querySelector("form").addEventListener("submit", function (event) {
        var content = editor.getValue();

        if (!content.trim()) {
            event.preventDefault();
            alert('Поле не может быть пустым!');
            return false;
        }

        textarea.value = content;
    });


});