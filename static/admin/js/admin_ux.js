/**
 * Admin UX Improvements (Standardized & Unified)
 * - Rename "Add" buttons for better UX
 * - Instant image previews (File/URL)
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

    // 2. Core Feature: Image Preview
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

        // Logic to find correct container (handles both standalone fields and tabular inlines)
        const row = input.closest('.form-row') || input.closest('tr') || input.closest('div');
        
        const updatePreview = (src) => {
            if (!src) return;
            let preview = row.querySelector('.instant-admin-preview');
            if (!preview) {
                preview = document.createElement('img');
                preview.className = 'instant-admin-preview';
                // Find a good place to insert it (at the end of the row/row-cell)
                row.appendChild(preview);
            }
            preview.src = src;
            preview.style.display = 'block';
            preview.onerror = () => { preview.style.display = 'none'; };
        };

        // Initial State
        if (input.type === 'file') {
            const currentLink = row.querySelector('.file-upload a, .readonly');
            if (currentLink && currentLink.href && /\.(jpg|jpeg|png|webp|gif|svg)$/i.test(currentLink.href)) {
                updatePreview(currentLink.href);
            }
        } else if (input.value && /^https?:\/\//i.test(input.value.trim())) {
            updatePreview(input.value.trim());
        }

        // Event Listeners
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
