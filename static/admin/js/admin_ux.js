
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
        const containers = document.querySelectorAll('.file-upload, .clearable-file-input');
    
        containers.forEach(container => {
            // Remove "Change:" text immediately on load
            const allNodes = Array.from(container.childNodes);
            allNodes.forEach(node => {
                if (node.nodeType === Node.TEXT_NODE && (node.textContent.includes('Change:') || node.textContent.includes('change:'))) {
                    node.textContent = '';
                }
            });

            const clearCheckbox = container.querySelector('input[type="checkbox"][name$="-clear"]');
            const fileInput = container.querySelector('input[type="file"]');
            if (!clearCheckbox || !fileInput) return;
    
            // Find the clear button/label
            const clearLabel =
                container.querySelector('label[for="' + clearCheckbox.id + '"]') ||
                container.querySelector('.btn-danger') ||
                container.querySelector('.clear-btn');
    
            // Gather "currently" nodes: text nodes + the file link
            const currentNodes = Array.from(container.childNodes).filter(n =>
                (n.nodeType === Node.TEXT_NODE && (
                    n.textContent.includes('Currently:') ||
                    n.textContent.includes('Change:')
                )) ||
                (n.nodeName === 'A' && n.href)
            );
    
            // Build the replacement upload button
            const uploadBtn = document.createElement('label');
            uploadBtn.htmlFor = fileInput.id || '';
            uploadBtn.className = 'btn btn-primary btn-sm mt-1';
            uploadBtn.style.display = 'none';
            uploadBtn.style.cursor = 'pointer';
            uploadBtn.textContent = '➕ Add New File';
            container.appendChild(uploadBtn);
    
            // Wire up the clear button
            if (clearLabel) {
                clearLabel.addEventListener('click', function () {
                    // 1. Hide the "Currently: <filename>" section
                    currentNodes.forEach(el => {
                        if (el.nodeType === Node.TEXT_NODE) el.textContent = '';
                        else el.style.display = 'none';
                    });
    
                    // 2. Hide the clear button itself
                    clearLabel.style.display = 'none';
    
                    // 3. Check the hidden checkbox so Django knows to clear
                    clearCheckbox.checked = true;
    
                    // 4. Reset any previously chosen file
                    fileInput.value = '';
    
                    // 5. Show the upload button instantly
                    uploadBtn.style.display = 'inline-block';
                    
                    // Force hide original file input to be replaced by our premium button if needed
                    fileInput.style.display = 'none';
                });
            }
        });
    }

    improveClearableFileInputs();
});
