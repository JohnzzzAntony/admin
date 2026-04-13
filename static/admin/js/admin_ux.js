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
     * 2. Instant Image Previews (File & URL)
     */
    function setupInstantPreviews(container = document) {
        // A. File Input Observer
        const fileInputs = container.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            if (input.dataset.previewInitialized) return;
            input.dataset.previewInitialized = "true";

            const handleFile = (file) => {
                if (file && file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        let preview = input.closest('.form-row').querySelector('.instant-admin-preview');
                        if (!preview) {
                            preview = document.createElement('img');
                            preview.className = 'instant-admin-preview';
                            input.closest('.form-row').appendChild(preview);
                        }
                        preview.src = e.target.result;
                    };
                    reader.readAsDataURL(file);
                }
            };

            input.addEventListener('change', e => handleFile(e.target.files[0]));

            // Initial preview for existing files
            const currentLink = input.closest('.form-row').querySelector('.file-upload a, .readonly');
            if (currentLink && currentLink.href && /\.(jpg|jpeg|png|webp|gif|svg)$/i.test(currentLink.href)) {
                let preview = input.closest('.form-row').querySelector('.instant-admin-preview');
                if (!preview) {
                    preview = document.createElement('img');
                    preview.className = 'instant-admin-preview';
                    input.closest('.form-row').appendChild(preview);
                }
                preview.src = currentLink.href;
            }
        });

        // B. URL Input Observer (Live Preview as you type)
        const urlSelectors = [
            '.field-image_url input', '.field-logo_url input', 
            '.field-banner_url input', '.field-favicon_url input',
            '.field-screenshot_url input', '.field-thumbnail_url input',
            '.field-hero_image_url input', '.field-icon_url input',
            '.field-bg_url input', '.field-img_url input',
            '.field-featured_image_url input', '.field-video_url input'
        ];
        const urlInputs = container.querySelectorAll(urlSelectors.join(','));
        
        urlInputs.forEach(input => {
            if (input.dataset.previewInitialized) return;
            input.dataset.previewInitialized = "true";

            const updatePreview = () => {
                const val = input.value.trim();
                if (val && (val.startsWith('http') || val.startsWith('/static'))) {
                    let preview = input.closest('.form-row').querySelector('.instant-admin-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'instant-admin-preview';
                        input.closest('.form-row').appendChild(preview);
                    }
                    preview.src = val;
                    preview.onerror = () => preview.style.display = 'none';
                    preview.onload = () => preview.style.display = 'block';
                }
            };

            input.addEventListener('input', updatePreview);
            updatePreview();
        });
    }

    /**
     * Init & Observation
     */
    function init() {
        renameButtons();
        setupInstantPreviews();
        
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) {
                        renameButtons(node);
                        setupInstantPreviews(node);
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
