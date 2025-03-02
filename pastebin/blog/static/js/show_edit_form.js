document.addEventListener("DOMContentLoaded", function () {

    function showEditForm(button) {
        document.getElementById('post-content-display').style.display = 'none';
        document.getElementById('edit-post-form').style.display = 'block';
        button.style.display = 'none';
        initializeEditor();
    }

    function initializeEditor() {
        var textarea = document.querySelector(".post-editor1 textarea");
        if (!textarea) return;

        var languageSelect = document.getElementById("language-select");

        var editor = CodeMirror.fromTextArea(textarea, {
            mode: languageSelect.value || "plaintext",
            lineNumbers: true,
            theme: "base16-light",
            indentUnit: 4,
            autoCloseBrackets: true,
            matchBrackets: true
        });

        editor.setValue(textarea.value);

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
    }

    var editButton = document.getElementById("edit-button");
    if (editButton) {
        editButton.addEventListener("click", function () {
            showEditForm(this);
        });
    }

});
