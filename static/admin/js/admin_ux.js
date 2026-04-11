
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
        const containers = document.querySelectorAll('.file-upload, .clearable-file-input, .field-image, .field-logo, .field-banner');
    
        containers.forEach(container => {
            if (container.dataset.enhanced === 'true') return;
            container.dataset.enhanced = 'true';

            const clearCheckbox = container.querySelector('input[type="checkbox"][name$="-clear"]');
            const fileInput = container.querySelector('input[type="file"]');
            if (!fileInput) return;
    
            // 1. Setup Preview Container
            const previewWrapper = document.createElement('div');
            previewWrapper.className = 'admin-preview-wrapper';
            previewWrapper.style.cssText = 'position:relative; display:inline-block; margin-top:10px; display:none;';
            
            const previewImg = document.createElement('img');
            previewImg.style.cssText = 'width:120px; height:120px; object-fit:cover; border-radius:12px; border:2px solid #e2e8f0; box-shadow:0 4px 6px rgba(0,0,0,0.1);';
            
            const closeBtn = document.createElement('button');
            closeBtn.type = 'button';
            closeBtn.className = 'admin-preview-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.style.cssText = 'position:absolute; top:-10px; right:-10px; width:28px; height:28px; background:#ef4444; color:#fff; border:none; border-radius:50%; cursor:pointer; font-weight:700; font-size:18px; line-height:1; display:flex; align-items:center; justify-content:center; box-shadow:0 2px 4px rgba(0,0,0,0.2); transition:all 0.2s;';
            
            previewWrapper.appendChild(previewImg);
            previewWrapper.appendChild(closeBtn);
            container.appendChild(previewWrapper);

            // 2. Handle Existing File (Currently)
            const currentNodes = Array.from(container.childNodes).filter(n =>
                (n.nodeType === Node.TEXT_NODE && (n.textContent.includes('Currently:') || n.textContent.includes('Change:'))) ||
                (n.nodeName === 'A' && n.href)
            );
            
            const existingLink = container.querySelector('a');
            if (existingLink && (existingLink.href.match(/\.(jpg|jpeg|png|gif|webp)$/i) || existingLink.textContent.match(/\.(jpg|jpeg|png|gif|webp)$/i))) {
                previewImg.src = existingLink.href;
                previewWrapper.style.display = 'inline-block';
                // Hide existing text/links
                currentNodes.forEach(el => {
                   if (el.nodeType === Node.TEXT_NODE) el.textContent = '';
                   else if (el.tagName === 'A') el.style.display = 'none';
                   else if (el.tagName === 'BR') el.remove();
                });
            }

            // 3. Label Cleanup (Hide "Change:")
            const allNodes = Array.from(container.childNodes);
            allNodes.forEach(node => {
                if (node.nodeType === Node.TEXT_NODE && (node.textContent.includes('Change:') || node.textContent.includes('change:'))) {
                    node.textContent = '';
                }
            });

            // 4. File Input change (New Upload)
            fileInput.addEventListener('change', function() {
                if (this.files && this.files[0]) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        previewImg.src = e.target.result;
                        previewWrapper.style.display = 'inline-block';
                        fileInput.style.display = 'none';
                    };
                    reader.readAsDataURL(this.files[0]);
                }
            });

            // 5. Close Button logic
            closeBtn.addEventListener('click', function() {
                previewWrapper.style.display = 'none';
                previewImg.src = '';
                fileInput.value = '';
                fileInput.style.display = 'inline-block';
                if (clearCheckbox) clearCheckbox.checked = true;
            });
            
            // 6. Handle original clear label if it exists
            const clearLabel = container.querySelector('label[for="' + (clearCheckbox ? clearCheckbox.id : '') + '"]');
            if (clearLabel) {
                clearLabel.style.display = 'none'; // Hide it as we have our own close btn
            }
        });
    }

    improveClearableFileInputs();
});
