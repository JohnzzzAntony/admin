/**
 * Admin UX Improvements (Standardized & Unified)
 * - Rename "Add" buttons for better UX
 * - Instant image previews (File/URL) with removal capability
 * - Dynamic mutation observer for formsets
 */

(function() {
    'use strict';

    // 1. UI Helper: Rename Buttons
    function renameButtons(container = document) {
        const addButtons = container.querySelectorAll('.addlink, .btn-success, .add-row a');
        addButtons.forEach(btn => {
            if (!btn.dataset.renamed && (btn.innerText.trim() === 'Add' || btn.innerText.trim().startsWith('Add '))) {
                btn.innerHTML = btn.innerHTML.replace('Add', '➕ Add New');
                btn.dataset.renamed = "true";
            }
        });
    }

    // 2. Core Feature: Image Preview with Removal
    function setupImagePreview(input) {
        if (!input || input.dataset.previewManaged) return;
        
        const isPotentialImage = (
            input.type === 'file' || 
            input.classList.contains('urlfield') || 
            input.classList.contains('vURLField') ||
            /image|logo|favicon|banner|icon|thumb|pic|img/i.test(input.name)
        );

        if (!isPotentialImage) return;
        input.dataset.previewManaged = "true";

        // Logic to find correct row container
        const row = input.closest('.form-row') || input.closest('tr') || input.closest('fieldset > div') || input.parentElement;
        
        const updatePreview = (src) => {
            if (!src) return;
            
            let container = row.querySelector('.admin-preview-container');
            if (!container) {
                container = document.createElement('div');
                container.className = 'admin-preview-container';
                
                const previewImg = document.createElement('img');
                previewImg.className = 'instant-admin-preview';
                container.appendChild(previewImg);
                
                const removeBtn = document.createElement('button');
                removeBtn.className = 'remove-preview-btn';
                removeBtn.innerHTML = '×';
                removeBtn.type = 'button';
                removeBtn.title = 'Remove image';
                
                removeBtn.onclick = (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    if (input.type === 'file') {
                        input.value = '';
                        // Find and check the Django 'Clear' checkbox if it exists
                        const clearCheckbox = row.querySelector('input[type="checkbox"][name*="-clear"]');
                        if (clearCheckbox) clearCheckbox.checked = true;
                    } else {
                        input.value = '';
                    }
                    
                    container.style.display = 'none';
                    // Trigger events to notify other potential listeners
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                };
                
                container.appendChild(removeBtn);
                row.appendChild(container);
            }
            
            const img = container.querySelector('.instant-admin-preview');
            img.src = src;
            container.style.display = 'inline-block';
            img.onerror = () => { container.style.display = 'none'; };

            // If we are showing a preview, ensure the clear checkbox is UNCHECKED
            const clearCheckbox = row.querySelector('input[type="checkbox"][name*="-clear"]');
            if (clearCheckbox) clearCheckbox.checked = false;
        };

        // Initial State (Existing images)
        if (input.type === 'file') {
            const currentLink = row.querySelector('.file-upload a, .readonly a');
            if (currentLink && currentLink.href && /\.(jpg|jpeg|png|webp|gif|svg)$/i.test(currentLink.href)) {
                updatePreview(currentLink.href);
            }
        } else if (input.value && /^https?:\/\//i.test(input.value.trim())) {
            updatePreview(input.value.trim());
        }

        // Event Listeners for changes
        input.addEventListener('change', function() {
            if (this.type === 'file' && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => updatePreview(e.target.result);
                reader.readAsDataURL(this.files[0]);
            } else if (this.value && /^https?:\/\//i.test(this.value.trim())) {
                updatePreview(this.value.trim());
            }
        });

        if (input.type !== 'file') {
            input.addEventListener('input', function() {
                if (this.value && /^https?:\/\//i.test(this.value.trim())) {
                    updatePreview(this.value.trim());
                } else if (!this.value) {
                    const container = row.querySelector('.admin-preview-container');
                    if (container) container.style.display = 'none';
                }
            });
        }
    }

    // 3. Orchestration
    function initialize(container = document) {
        renameButtons(container);
        container.querySelectorAll('input').forEach(setupImagePreview);
    }

    function init() {
        initialize();

        // Observe dynamic additions (e.g., adding rows to inlines)
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) {
                        initialize(node);
                    }
                });
            });
        });

        const target = document.getElementById('content') || document.body;
        observer.observe(target, { childList: true, subtree: true });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
