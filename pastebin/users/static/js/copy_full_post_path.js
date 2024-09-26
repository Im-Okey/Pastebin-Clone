function copyToClipboard(url) {
    const tempInput = document.createElement('input');
    tempInput.value = window.location.origin + url;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);

    alert('URL скопирован в буфер обмена!');
}