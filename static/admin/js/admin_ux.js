
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

    // 3. Clearable File Input Improvements
    function improveClearableFileInputs() {
        const fileUploads = document.querySelectorAll('.file-upload, .clearable-file-input');
        
        fileUploads.forEach(container => {
            // 1. Remove the "Change:" text node entirely
            const nodes = Array.from(container.childNodes);
            nodes.forEach(node => {
                if (node.nodeType === Node.TEXT_NODE && (node.textContent.includes('Change:') || node.textContent.includes('change:'))) {
                    node.textContent = '';
                }
            });

            // 2. Identify core elements
            const clearCheckbox = container.querySelector('input[type="checkbox"][name$="-clear"]');
            const currentlySection = Array.from(container.childNodes).filter(n => 
                (n.nodeType === Node.TEXT_NODE && n.textContent.includes('Currently:')) || 
                (n.tagName === 'A' && n.href && !n.classList.contains('btn'))
            );
            
            // The file input itself
            const fileInput = container.querySelector('input[type="file"]');
            
            if (clearCheckbox && fileInput) {
                // Find the label for the checkbox (often styled as a Clear button in Jazzmin)
                const clearLabel = container.querySelector('label[for="' + clearCheckbox.id + '"]') || 
                                 container.querySelector('.btn-danger') || 
                                 container.querySelector('.clear-btn');

                if (clearLabel) {
                    clearLabel.addEventListener('click', function(e) {
                         // Instant removal from UI
                         currentlySection.forEach(el => {
                             if (el.nodeType === Node.TEXT_NODE) el.textContent = '';
                             else if (el.nodeType === Node.ELEMENT_NODE) el.style.display = 'none';
                         });
                         
                         // Hide the clear button itself after use
                         clearLabel.style.display = 'none';
                         
                         // Move file input to a prominent position if needed, or just let it stay
                         fileInput.classList.add('btn-primary-upload');
                         
                         // We don't prevent default, because we want the checkbox to actually be checked for the backend
                    });
                }
            }
        });
    }

    improveClearableFileInputs();
});
