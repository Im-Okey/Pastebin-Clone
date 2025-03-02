let selectedTags = [];

document.addEventListener("DOMContentLoaded", function () {
    // Получаем уже выбранные теги из значения поля (если они есть)
    let existingTags = document.getElementById("tagsField").value;
    if (existingTags) {
        selectedTags = existingTags.split(", ").map(tag => tag.trim());
    }

    // Обновляем отображение выбранных тегов
    updateSelectedTags();
});

// Функция для показа/скрытия списка тегов
function toggleTagList() {
    const tagListContainer = document.getElementById('tagListContainer');
    const currentDisplay = tagListContainer.style.display;
    tagListContainer.style.display = currentDisplay === 'none' || currentDisplay === '' ? 'block' : 'none';
}

// Функция для выбора/отмены выбора тега
function selectTag(tagName) {
    const tagIndex = selectedTags.indexOf(tagName);

    if (tagIndex === -1) {
        selectedTags.push(tagName);
    } else {
        selectedTags.splice(tagIndex, 1);
    }

    // Обновляем отображение выбранных тегов
    updateSelectedTags();

    // Обновляем скрытое поле, чтобы оно отправляло выбранные теги
    updateTagsField();
}

// Функция для обновления отображаемого списка выбранных тегов
function updateSelectedTags() {
    const selectedTagsContainer = document.getElementById('selectedTags');
    selectedTagsContainer.innerHTML = '';

    selectedTags.forEach(tag => {
        const tagElement = document.createElement('div');
        tagElement.classList.add('selected-tag');
        tagElement.innerHTML = `${tag} <span class="remove-tag" onclick="removeTag('${tag}')">&times;</span>`;
        selectedTagsContainer.appendChild(tagElement);
    });

    // Обновляем стиль для каждого тега в списке
    document.querySelectorAll('.tag').forEach(element => {
        if (selectedTags.includes(element.textContent.trim().replace('+ ', ''))) {
            element.classList.add('tag-selected');
        } else {
            element.classList.remove('tag-selected');
        }
    });
}

// Функция для удаления выбранного тега
function removeTag(tagName) {
    const tagIndex = selectedTags.indexOf(tagName);
    if (tagIndex !== -1) {
        selectedTags.splice(tagIndex, 1);
        updateSelectedTags();
        updateTagsField();
    }
}

// Функция для обновления скрытого поля с тегами
function updateTagsField() {
    // Обновляем значение скрытого поля для отправки данных
    const tagsField = document.getElementById('tagsField');
    tagsField.value = selectedTags.join(', ');

    // Обновляем отображаемое поле (если нужно)
    const tagsFieldDisplay = document.getElementById('tagsFieldDisplay');
    tagsFieldDisplay.value = selectedTags.join(', ');
}
