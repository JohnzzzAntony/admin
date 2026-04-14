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

        // Find the most specific container for this field
        const fieldContainer = input.closest('.fieldBox') || input.closest('.form-group') || input.closest('.form-row > div') || input.parentElement;
        
        const updatePreview = (src) => {
            if (!src) return;
            
            let container = fieldContainer.querySelector('.admin-preview-container');
            if (!container) {
                container = document.createElement('div');
                container.className = 'admin-preview-container';
                
                const previewImg = document.createElement('img');
                previewImg.className = 'instant-admin-preview';
                // Styles are mostly handled by admin_premium.css, but we ensure basic visibility here
                previewImg.style.display = 'block';
                container.appendChild(previewImg);
                
                const removeBtn = document.createElement('button');
                removeBtn.className = 'remove-preview-btn';
                removeBtn.innerHTML = '×';
                removeBtn.type = 'button';
                removeBtn.title = 'Remove image';
                
                removeBtn.onclick = (e) => {
                    e.preventDefault();
                    if (input.type === 'file') {
                        input.value = '';
                        // Clear text nodes and links that Django might show for currently selected files
                        const clearCheckbox = fieldContainer.querySelector('input[type="checkbox"][name*="-clear"]');
                        if (clearCheckbox) clearCheckbox.checked = true;
                        
                        // Hide bits of the default Django widget that show the old filename
                        fieldContainer.querySelectorAll('a, .file-upload, span.clearable-file-input').forEach(el => {
                            if (!el.contains(input)) el.style.display = 'none';
                        });
                        
                        // If there are text nodes containing filenames (like in some custom themes), clear them
                        const walker = document.createTreeWalker(fieldContainer, NodeFilter.SHOW_TEXT, null, false);
                        let node;
                        while(node = walker.nextNode()) {
                            if (node.textContent.includes('.') && /\.(webp|jpg|png|jpeg|gif)$/i.test(node.textContent)) {
                                node.textContent = '';
                            }
                        }
                    } else {
                        input.value = '';
                    }
                    container.style.display = 'none';
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                };
                
                container.appendChild(removeBtn);
                
                // Smart Insertion: after label or at the top of the field
                const label = fieldContainer.querySelector('label');
                if (label) {
                    label.after(container);
                } else {
                    fieldContainer.prepend(container);
                }
            }
            
            const img = container.querySelector('.instant-admin-preview');
            img.src = src;
            container.style.display = 'inline-block';
            img.onerror = () => { container.style.display = 'none'; };

            const clearCheckbox = fieldContainer.querySelector('input[type="checkbox"][name*="-clear"]');
            if (clearCheckbox) clearCheckbox.checked = false;
        };

        // Initial State (Existing images)
        if (input.type === 'file') {
            // Search specifically within this field's container
            const currentLink = fieldContainer.querySelector('a[href*="/media/"], .file-upload a, .readonly a, .clearable-file-input a');
            if (currentLink && currentLink.href && /\.(jpg|jpeg|png|webp|gif|svg|avif|ico)$/i.test(currentLink.href.split('?')[0])) {
                updatePreview(currentLink.href);
            }
        } else if (input.value && /^https?:\/\//i.test(input.value.trim())) {
            updatePreview(input.value.trim());
        }

        // Live Changes
        input.addEventListener('change', function() {
            if (this.type === 'file' && this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => updatePreview(e.target.result);
                reader.readAsDataURL(this.files[0]);
            } else if (this.value && /^https?:\/\//i.test(this.value.trim())) {
                updatePreview(this.value.trim());
            }
        });

        // URL fields: live preview as user types
        if (input.type !== 'file') {
            input.addEventListener('input', function() {
                if (this.value && /^https?:\/\//i.test(this.value.trim())) {
                    updatePreview(this.value.trim());
                } else if (!this.value) {
                    const container = fieldContainer.querySelector('.admin-preview-container');
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
