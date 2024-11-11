let selectedTags = [...document.getElementById('tagsField').value.split(',').filter(tag => tag)];

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

function updateTagsField() {
    document.getElementById('tagsField').value = selectedTags.join(',');
}

function applyFilters() {
    document.querySelector('form').submit();
}