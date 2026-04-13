/**
 * Admin UX Improvements (Hardened & Optimized)
 * - Rename "Add" buttons to "➕ Add New"
 * - Rename "Change" buttons to "📋 Manage"
 * - MutationObserver for dynamic content (formsets, AJAX)
 * - Premium clearable file input previews
 */

(function() {
    'use strict';

    /**
     * 1. Rename Buttons
     */
    function renameButtons(container = document) {
        // Add buttons
        const addButtons = container.querySelectorAll('.addlink, .btn-success, .add-row a');
        addButtons.forEach(btn => {
            const text = btn.innerText.trim();
            if ((text === 'Add' || text.startsWith('Add ')) && !btn.innerText.includes('➕')) {
                btn.innerHTML = btn.innerHTML.replace('Add', '➕ Add New');
            }
        });

        // Change/View buttons in list
        const changeLinks = container.querySelectorAll('.changelink, .btn-info');
        changeLinks.forEach(link => {
            if (link.innerText.trim() === 'Change') {
                link.innerHTML = '📋 Manage';
            }
        });
    }

    /**
     * 2. Clearable File Input Improvements
     */
    function improveClearableFileInputs(container = document) {
        const selector = '.file-upload, .clearable-file-input, .field-image, .field-logo, .field-banner, .field-image_url, td.field-image, td.column-image, td.field-image_url';
        const elements = container.querySelectorAll(selector);

        elements.forEach(containerEl => {
            if (containerEl.dataset.enhanced === 'true') return;

            const fileInput = containerEl.querySelector('input[type="file"]');
            const urlInput = containerEl.querySelector('input[type="url"], input[name$="image_url"]');
            const clearCheckbox = containerEl.querySelector('input[type="checkbox"][name$="-clear"]');

            if (!fileInput && !urlInput) return;
            containerEl.dataset.enhanced = 'true';

            // Setup Preview Container
            const previewWrapper = document.createElement('div');
            previewWrapper.className = 'admin-preview-wrapper';
            
            const previewImg = document.createElement('img');
            previewImg.className = 'admin-preview-img';
            
            const fileNameLabel = document.createElement('span');
            fileNameLabel.className = 'admin-preview-label';

            const closeBtn = document.createElement('button');
            closeBtn.type = 'button';
            closeBtn.className = 'admin-preview-close';
            closeBtn.innerHTML = '&times;';
            
            previewWrapper.appendChild(previewImg);
            previewWrapper.appendChild(fileNameLabel);
            previewWrapper.appendChild(closeBtn);
            containerEl.appendChild(previewWrapper);

            let chooseBtn = null;
            if (fileInput) {
                fileInput.style.display = 'none';
                if (clearCheckbox) clearCheckbox.style.display = 'none';
                
                chooseBtn = document.createElement('label');
                chooseBtn.htmlFor = fileInput.id;
                chooseBtn.className = 'admin-choose-btn';
                chooseBtn.innerHTML = '<i class="fas fa-plus-circle"></i> Upload Image';
                containerEl.appendChild(chooseBtn);
            }

            function updateVisibility(hasImage, src, labelText) {
                if (hasImage) {
                    previewImg.src = src;
                    fileNameLabel.textContent = labelText;
                    previewWrapper.style.display = 'flex';
                    if (chooseBtn) chooseBtn.style.display = 'none';
                    if (clearCheckbox) clearCheckbox.checked = false;
                } else {
                    previewWrapper.style.display = 'none';
                    previewImg.src = '';
                    if (chooseBtn) chooseBtn.style.display = 'inline-block';
                    if (clearCheckbox) clearCheckbox.checked = true;
                }
            }

            // Initial State
            const existingLink = containerEl.querySelector('a');
            if (existingLink && existingLink.href.match(/\.(jpg|jpeg|png|gif|webp|svg)/i)) {
                updateVisibility(true, existingLink.href, existingLink.textContent.split('/').pop());
                
                // Cleanup Django text
                Array.from(containerEl.childNodes).forEach(n => {
                    if (n.nodeType === Node.TEXT_NODE && (n.textContent.includes('Currently:') || n.textContent.includes('Change:'))) {
                        n.textContent = '';
                    }
                    if (['A', 'BR', 'SPAN'].includes(n.tagName) && n !== previewWrapper && !previewWrapper.contains(n)) {
                        n.style.display = 'none';
                    }
                });
            } else if (urlInput && urlInput.value) {
                updateVisibility(true, urlInput.value, 'External URL');
            }

            // Events
            fileInput && fileInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = (e) => updateVisibility(true, e.target.result, this.files[0].name);
                    reader.readAsDataURL(this.files[0]);
                }
            });

            urlInput && urlInput.addEventListener('input', function() {
                if (this.value && this.value.match(/\.(jpg|jpeg|png|gif|webp|svg)/i)) {
                    updateVisibility(true, this.value, 'From URL');
                } else if (!this.value) {
                    updateVisibility(false);
                }
            });

            closeBtn.addEventListener('click', () => {
                updateVisibility(false);
                if (fileInput) fileInput.value = '';
                if (urlInput) urlInput.value = '';
            });
        });
    }

    /**
     * Init & Observation
     */
    function init() {
        renameButtons();
        improveClearableFileInputs();
        
        // Setup MutationObserver for dynamic elements
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // ELEMENT_NODE
                        renameButtons(node);
                        improveClearableFileInputs(node);
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

