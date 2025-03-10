let selectedTags = [];

// Функция для сворачивания/разворачивания списка тегов
function toggleTagList() {
    const tagListContainer = document.getElementById('tagListContainer');
    const currentDisplay = tagListContainer.style.display;
    tagListContainer.style.display = currentDisplay === 'none' || currentDisplay === '' ? 'block' : 'none';
}

function selectTag(tagName) {
    const tagIndex = selectedTags.indexOf(tagName);

    if (tagIndex === -1) {
        selectedTags.push(tagName);
    } else {
        selectedTags.splice(tagIndex, 1);
    }

    updateSelectedTags();
    updateTagsField();
}


function updateSelectedTags() {
    const selectedTagsContainer = document.getElementById('selectedTags');
    selectedTagsContainer.innerHTML = '';

    selectedTags.forEach(tag => {
        const tagElement = document.createElement('div');
        tagElement.classList.add('selected-tag');
        tagElement.innerHTML = `${tag} <span class="remove-tag" onclick="removeTag('${tag}')">&times;</span>`;
        selectedTagsContainer.appendChild(tagElement);
    });

    document.querySelectorAll('.tag').forEach(element => {
        if (selectedTags.includes(element.textContent.trim().replace('+ ', ''))) {
            element.classList.add('tag-selected');
        } else {
            element.classList.remove('tag-selected');
        }
    });
}

function removeTag(tagName) {
    const tagIndex = selectedTags.indexOf(tagName);
    if (tagIndex !== -1) {
        selectedTags.splice(tagIndex, 1);
        updateSelectedTags();
        updateTagsField();
    }
}

// Обновление поля с тегами в форме
function updateTagsField() {
    // Обновляем значение заблокированного поля с тегами через запятую
    const tagsField = document.getElementById('id_tags'); // Это ID поля формы
    tagsField.value = selectedTags.join(', ');

    const tagsField1 = document.getElementById('tagsField'); // Это ID поля формы
    tagsField1.value = selectedTags.join(', ');
}
