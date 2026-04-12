
/**
 * Admin UX Improvements
 * - Rename "Add" buttons to "➕ Add New"
 * - Rename "Change" buttons to "📋 Manage"
 * - Touch-friendly improvements
 */

document.addEventListener('DOMContentLoaded', function() {
    // 1. Rename Buttons
    function renameButtons() {
        // Add buttons
        const addButtons = document.querySelectorAll('.addlink, .btn-success, .add-row a');
        addButtons.forEach(btn => {
            if (btn.innerText.trim() === 'Add' || btn.innerText.includes('Add ')) {
                 if (!btn.innerText.includes('➕')) {
                    btn.innerHTML = btn.innerHTML.replace('Add', '➕ Add New');
                 }
            }
        });

        // Change/View buttons in list
        const changeLinks = document.querySelectorAll('.changelink, .btn-info');
        changeLinks.forEach(link => {
            if (link.innerText.trim() === 'Change') {
                link.innerHTML = '📋 Manage';
            }
        });
        
        // Save buttons
        const saveButtons = document.querySelectorAll('input[name="_save"], button[name="_save"]');
        saveButtons.forEach(btn => {
            if (btn.value === 'Save' || btn.innerText.trim() === 'Save') {
                // Keep save as is or improve? User only asked for Add and Change.
            }
        });
    }

    renameButtons();

    // 2. Mobile Friendly Tables
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        if (!table.parentElement.classList.contains('table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });

    // 3. Clearable File Input Improvements & Dynamic Previews
    function improveClearableFileInputs() {
        const selector = '.file-upload, .clearable-file-input, .field-image, .field-logo, .field-banner, .field-image_url, td.field-image, td.column-image, td.field-image_url';
        const containers = document.querySelectorAll(selector);
    
        containers.forEach(container => {
            if (container.dataset.enhanced === 'true') return;
            
            const fileInput = container.querySelector('input[type="file"]');
            const urlInput = container.querySelector('input[type="url"], input[name$="image_url"]');
            const clearCheckbox = container.querySelector('input[type="checkbox"][name$="-clear"]');
            
            if (!fileInput && !urlInput) return;
            container.dataset.enhanced = 'true';

            // 1. Setup Preview Container (Hidden by default)
            const previewWrapper = document.createElement('div');
            previewWrapper.className = 'admin-preview-wrapper';
            previewWrapper.style.cssText = 'position:relative; display:flex; flex-direction:column; align-items:flex-start; margin-top:10px; display:none;';
            
            const previewImg = document.createElement('img');
            previewImg.style.cssText = 'width:120px; height:120px; object-fit:cover; border-radius:12px; border:2px solid #e2e8f0; background:#f8fafc;';
            
            const fileNameLabel = document.createElement('span');
            fileNameLabel.style.cssText = 'font-size: 0.75rem; color: #64748b; margin-top: 5px; font-weight: 500; max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;';

            const closeBtn = document.createElement('button');
            closeBtn.type = 'button';
            closeBtn.className = 'admin-preview-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.style.cssText = 'position:absolute; top:-10px; left:105px; width:28px; height:28px; background:#ef4444; color:#fff; border:none; border-radius:50%; cursor:pointer; font-weight:700; z-index:10; display:flex; align-items:center; justify-content:center; box-shadow:0 2px 4px rgba(0,0,0,0.2);';
            
            previewWrapper.appendChild(previewImg);
            previewWrapper.appendChild(fileNameLabel);
            previewWrapper.appendChild(closeBtn);
            container.appendChild(previewWrapper);

            // 2. Hide ugly default parts and create "Choose" button
            let chooseBtn = null;
            if (fileInput) {
                fileInput.style.display = 'none';
                clearCheckbox && (clearCheckbox.style.display = 'none');
                
                chooseBtn = document.createElement('label');
                chooseBtn.htmlFor = fileInput.id;
                chooseBtn.className = 'btn btn-sm btn-light border';
                chooseBtn.style.cssText = 'cursor:pointer; display:inline-block; padding: 8px 16px; border-radius: 10px; font-size: 0.85rem; font-weight:600;';
                chooseBtn.innerHTML = '<i class="fas fa-plus-circle mr-1"></i> Upload Image';
                container.appendChild(chooseBtn);
            }

            // Function to update visibility
            function updateVisibility(hasImage, src, labelText) {
                if (hasImage) {
                    previewImg.src = src;
                    fileNameLabel.textContent = labelText;
                    previewWrapper.style.display = 'flex';
                    if (chooseBtn) chooseBtn.style.display = 'none';
                } else {
                    previewWrapper.style.display = 'none';
                    previewImg.src = '';
                    if (chooseBtn) chooseBtn.style.display = 'inline-block';
                    if (clearCheckbox) clearCheckbox.checked = true;
                }
            }

            // 3. Initial State Check
            const existingLink = container.querySelector('a');
            if (existingLink && existingLink.href.match(/\.(jpg|jpeg|png|gif|webp|svg)/i)) {
                updateVisibility(true, existingLink.href, existingLink.textContent.split('/').pop());
                
                // Remove messy Django text
                container.childNodes.forEach(n => {
                    if (n.nodeType === Node.TEXT_NODE && (n.textContent.includes('Currently:') || n.textContent.includes('Change:'))) n.textContent = '';
                    if (n.tagName === 'A' || n.tagName === 'BR' || n.tagName === 'SPAN') {
                       if (n !== previewWrapper && !previewWrapper.contains(n)) n.style.display = 'none';
                    }
                });
            } else if (urlInput && urlInput.value) {
                updateVisibility(true, urlInput.value, 'External URL');
            }

            // 4. Input Handlers
            fileInput && fileInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = (e) => updateVisibility(true, e.target.result, fileInput.files[0].name);
                    reader.readAsDataURL(this.files[0]);
                    if (clearCheckbox) clearCheckbox.checked = false;
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
            
            // Final removal of any leftover clear labels
            const clearLabel = container.querySelector('label[for="' + (clearCheckbox ? clearCheckbox.id : '') + '"]');
            if (clearLabel) clearLabel.style.display = 'none';
        });
    }

    improveClearableFileInputs();

    // Re-run whenever a new formset row is added (using django.jQuery)
    if (window.django && django.jQuery) {
        django.jQuery(document).on('formset:added', function() {
            setTimeout(improveClearableFileInputs, 100);
        });
    }
});
