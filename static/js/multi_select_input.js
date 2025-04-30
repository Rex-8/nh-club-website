/**
 * MultiSelectInput - Minimal tag input system core logic
 */
class MultiSelectInput {
    constructor(containerSelector, availableTags = [], onTagsChanged = null) {
      this.container = document.querySelector(containerSelector);
      if (!this.container) {
        console.error(`Container element not found: ${containerSelector}`);
        return;
      }
  
      this.availableTags = availableTags;
      this.selectedTags = [];
      this.onTagsChanged = onTagsChanged;
  
      this.createElements();
      this.bindEvents();
    }
  
    createElements() {
      this.tagDisplay = document.createElement('div');
      this.controls = document.createElement('div');
      this.tagSelect = document.createElement('select');
  
      const defaultOption = document.createElement('option');
      defaultOption.value = '';
      defaultOption.textContent = 'Select a tag';
      defaultOption.disabled = true;
      defaultOption.selected = true;
      this.tagSelect.appendChild(defaultOption);
  
      this.availableTags.forEach(tag => {
        const option = document.createElement('option');
        option.value = tag;
        option.textContent = tag;
        this.tagSelect.appendChild(option);
      });
  
      this.addButton = document.createElement('button');
      this.addButton.textContent = '+ Add Tag';
  
      this.controls.appendChild(this.tagSelect);
      this.controls.appendChild(this.addButton);
      this.container.appendChild(this.tagDisplay);
      this.container.appendChild(this.controls);
    }
  
    bindEvents() {
      this.addButton.addEventListener('click', () => this.addTag());
  
      this.tagSelect.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          this.addTag();
        }
      });
    }
  
    addTag() {
      const tagValue = this.tagSelect.value;
      if (!tagValue || this.selectedTags.includes(tagValue)) return;
  
      const tagEl = document.createElement('span');
      tagEl.textContent = tagValue;
  
      const removeBtn = document.createElement('span');
      removeBtn.textContent = ' ×';
      removeBtn.style.cursor = 'pointer';
      removeBtn.addEventListener('click', () => this.removeTag(tagEl, tagValue));
  
      tagEl.appendChild(removeBtn);
      this.tagDisplay.appendChild(tagEl);
      this.tagDisplay.appendChild(document.createTextNode(' '));
  
      this.selectedTags.push(tagValue);
      this.tagSelect.selectedIndex = 0;
  
      if (this.onTagsChanged) this.onTagsChanged(this.selectedTags);
    }
  
    removeTag(tagElement, tagValue) {
      this.tagDisplay.removeChild(tagElement);
      const index = this.selectedTags.indexOf(tagValue);
      if (index !== -1) this.selectedTags.splice(index, 1);
      if (this.onTagsChanged) this.onTagsChanged(this.selectedTags);
    }
  
    getTags() {
      return [...this.selectedTags];
    }
  
    setTags(tags) {
      this.tagDisplay.innerHTML = '';
      this.selectedTags = [];
  
      tags.forEach(tag => {
        for (let i = 0; i < this.tagSelect.options.length; i++) {
          if (this.tagSelect.options[i].value === tag) {
            this.tagSelect.selectedIndex = i;
            break;
          }
        }
        this.addTag();
      });
    }
  }
  