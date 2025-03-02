document.addEventListener("DOMContentLoaded", function () {
    var textarea = document.querySelector(".post-editor textarea");
    var editor = CodeMirror.fromTextArea(textarea, {
        mode: "plaintext",
        lineNumbers: true,
        theme: "base16-light",
        indentUnit: 4
    });

    document.getElementById("language-select").addEventListener("change", function () {
        var mode = this.value;
        editor.setOption("mode", mode === "plaintext" ? null : mode);
    });

});