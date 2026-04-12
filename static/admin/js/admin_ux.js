
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
            
            if (!fileInput && !urlInput) return;
            container.dataset.enhanced = 'true';

            const clearCheckbox = container.querySelector('input[type="checkbox"][name$="-clear"]');
    
            // 1. Setup Preview Container
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
            if (fileInput) {
                fileInput.style.display = 'none';
                const chooseBtn = document.createElement('label');
                chooseBtn.htmlFor = fileInput.id;
                chooseBtn.className = 'btn btn-sm btn-outline-primary';
                chooseBtn.style.cssText = 'cursor:pointer; display:inline-block; padding: 6px 12px; border-radius: 8px; font-size: 0.85rem;';
                chooseBtn.innerHTML = '<i class="fas fa-image"></i> Choose Image';
                container.appendChild(chooseBtn);
                container.dataset.chooseBtn = 'true';
            }

            // 3. Handle Existing File
            const existingLink = container.querySelector('a');
            if (existingLink && existingLink.href.match(/\.(jpg|jpeg|png|gif|webp)$/i)) {
                previewImg.src = existingLink.href;
                fileNameLabel.textContent = existingLink.textContent.split('/').pop();
                previewWrapper.style.display = 'flex';
                if (container.querySelector('label[class*="btn-outline-primary"]')) {
                    container.querySelector('label[class*="btn-outline-primary"]').style.display = 'none';
                }
                // Hide Django standard text
                container.childNodes.forEach(n => {
                    if (n.nodeType === Node.TEXT_NODE && (n.textContent.includes('Currently:') || n.textContent.includes('Change:'))) n.textContent = '';
                    if (n.tagName === 'A' || n.tagName === 'BR') n.style.display = 'none';
                });
            } else if (urlInput && urlInput.value) {
                // Initial URL preview
                previewImg.src = urlInput.value;
                fileNameLabel.textContent = 'From URL';
                previewWrapper.style.display = 'flex';
            }

            // 4. File Input change
            if (fileInput) {
                fileInput.addEventListener('change', function() {
                    if (this.files && this.files[0]) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            previewImg.src = e.target.result;
                            fileNameLabel.textContent = fileInput.files[0].name;
                            previewWrapper.style.display = 'flex';
                            const btn = container.querySelector('label[class*="btn-outline-primary"]');
                            if (btn) btn.style.display = 'none';
                        };
                        reader.readAsDataURL(this.files[0]);
                    }
                });
            }

            // 5. URL Input change
            if (urlInput) {
                urlInput.addEventListener('input', function() {
                    if (this.value && this.value.match(/\.(jpg|jpeg|png|gif|webp)/i)) {
                        previewImg.src = this.value;
                        fileNameLabel.textContent = 'From URL';
                        previewWrapper.style.display = 'flex';
                    }
                });
            }

            // 6. Close Button logic
            closeBtn.addEventListener('click', function() {
                previewWrapper.style.display = 'none';
                previewImg.src = '';
                if (fileInput) {
                    fileInput.value = '';
                    const btn = container.querySelector('label[class*="btn-outline-primary"]');
                    if (btn) btn.style.display = 'inline-block';
                }
                if (urlInput) urlInput.value = '';
                if (clearCheckbox) clearCheckbox.checked = true;
            });
            
            // 7. Cleanup standard clear label
            const clearLabel = container.querySelector('label[for="' + (clearCheckbox ? clearCheckbox.id : '') + '"]');
            if (clearLabel) clearLabel.style.display = 'none';
        });
    }

    improveClearableFileInputs();

    // Re-run whenever a new formset row is added
    $(document).on('formset:added', function() {
        setTimeout(improveClearableFileInputs, 100);
    });
});
