let selectedTags = [];

document.addEventListener("DOMContentLoaded", function () {
    let existingTags = document.getElementById("tagsField").value;
    if (existingTags) {
        selectedTags = existingTags.split(", ").map(tag => tag.trim());
    }

    updateSelectedTags();
});

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

    // Обновляем стиль для каждого тега в списке
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

function updateTagsField() {
    const tagsField = document.getElementById('tagsField');
    tagsField.value = selectedTags.join(', ');

    const tagsFieldDisplay = document.getElementById('tagsFieldDisplay');
    tagsFieldDisplay.value = selectedTags.join(', ');
}
