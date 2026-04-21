/**
 * Admin UX — Clean & Simple
 * - Live image preview thumbnails on file inputs
 * - REMOVE button replacing delete checkbox in tabular inlines
 * - Rename add-row link to "+ Add New Image"
 * - MutationObserver for dynamically added rows
 */

(function () {
    'use strict';

    /* ─────────────────────────────────────────────
       1. LIVE IMAGE PREVIEW  (only on change-form fields, NOT inside tabular inline)
       ───────────────────────────────────────────── */
    function setupChangeFormPreview(input) {
        if (!input || input.dataset.previewManaged) return;

        // Previews enabled for all image fields including tabular

        const isImageField = (
            input.type === 'file' ||
            /image|logo|favicon|banner|icon|thumb|pic|img/i.test(input.name)
        );
        if (!isImageField) return;

        input.dataset.previewManaged = 'true';

        const fieldBox = input.closest('.fieldBox') || input.closest('.form-group') || input.parentElement;

        const showPreview = (src) => {
            if (!src) return;
            let wrap = fieldBox.querySelector('.admin-preview-container');
            if (!wrap) {
                wrap = document.createElement('div');
                wrap.className = 'admin-preview-container';

                const img = document.createElement('img');
                img.className = 'instant-admin-preview';
                wrap.appendChild(img);

                const btn = document.createElement('button');
                btn.className = 'remove-preview-btn';
                btn.innerHTML = '&times;';
                btn.type = 'button';
                btn.title = 'Remove image';
                btn.addEventListener('click', () => {
                    input.value = '';
                    const cb = fieldBox.querySelector('input[type="checkbox"][name*="-clear"]');
                    if (cb) {
                        cb.checked = true;
                        // Trigger change event to fire setupInstantClear's update logic
                        cb.dispatchEvent(new Event('change'));
                    }
                });
                wrap.appendChild(btn);

                const label = fieldBox.querySelector('label');
                if (label) label.after(wrap);
                else fieldBox.prepend(wrap);
            }
            const imgEl = wrap.querySelector('.instant-admin-preview');
            imgEl.src = src;
            wrap.style.display = 'inline-block';
            imgEl.onerror = () => { wrap.style.display = 'none'; };

            const cb = fieldBox.querySelector('input[type="checkbox"][name*="-clear"]');
            if (cb) cb.checked = false;
        };

        // Show existing image on load
        if (input.type === 'file') {
            const link = fieldBox.querySelector('a[href*="/media/"]');
            if (link && /\.(jpg|jpeg|png|webp|gif|svg|avif|ico)$/i.test(link.href.split('?')[0])) {
                showPreview(link.href);
            }
        }

        // Show on file selection
        input.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => showPreview(e.target.result);
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

    /* ─────────────────────────────────────────────
       INSTANT CLEAR FUNCTIONALITY
       ───────────────────────────────────────────── */
    function setupInstantClear(checkbox) {
        if (!checkbox || checkbox.dataset.clearManaged) return;
        
        // Target both field-clearing and inline-row deletion
        const isClear = checkbox.name && checkbox.name.includes('-clear');
        const isDelete = checkbox.name && checkbox.name.endsWith('-DELETE');
        
        if (!isClear && !isDelete) return;

        checkbox.dataset.clearManaged = 'true';
        
        // Find the most appropriate container to strike
        // (td for tabular rows, form-row for standard fields)
        const container = checkbox.closest('tr') || checkbox.closest('.form-row') || checkbox.closest('p') || checkbox.parentElement;
        
        const updateVisibility = () => {
            const isChecked = checkbox.checked;
            
            // 1. Strike the immediate container/row
            if (isChecked) {
                container.classList.add('clearing-active');
            } else {
                container.classList.remove('clearing-active');
            }

            // 2. Strike related previews elsewhere on the page
            // (e.g., if we clear 'image', also strike the 'preview' readonly field)
            if (isClear) {
                const fieldName = checkbox.name.replace('-clear', '');
                // Standard naming patterns for previews in this project
                const selectors = [
                    `.field-preview`, 
                    `.field-thumbnail`, 
                    `.field-${fieldName}_preview`,
                    `.field-brand_logo`
                ];
                selectors.forEach(sel => {
                    const related = document.querySelectorAll(sel);
                    related.forEach(el => {
                        isChecked ? el.classList.add('clearing-active') : el.classList.remove('clearing-active');
                    });
                });
            }
        };

        checkbox.addEventListener('change', updateVisibility);
        
        // Initial state (useful if page reloads with errors)
        updateVisibility();

        // If a new file is selected, automatically uncheck the "Clear" box
        const fileInput = container.querySelector('input[type="file"]');
        if (fileInput) {
            fileInput.addEventListener('change', function() {
                if (this.files && this.files.length > 0) {
                    checkbox.checked = false;
                    updateVisibility();
                }
            });
        }
    }

    /* ─────────────────────────────────────────────
       4. ORCHESTRATE
       ───────────────────────────────────────────── */
    function initialize(root = document) {
        // Change-form previews (non-tabular)
        root.querySelectorAll('input').forEach(input => {
            setupChangeFormPreview(input);
            if (input.type === 'checkbox') setupInstantClear(input);
        });
    }

    function init() {
        initialize();

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mut) => {
                mut.addedNodes.forEach((node) => {
                    if (node.nodeType !== 1) return;
                    node.querySelectorAll && node.querySelectorAll('input').forEach(input => {
                        setupChangeFormPreview(input);
                        if (input.type === 'checkbox') setupInstantClear(input);
                    });
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
