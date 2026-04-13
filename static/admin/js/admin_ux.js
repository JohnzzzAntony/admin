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
     * Init & Observation
     */
    function init() {
        renameButtons();
        
        // Setup MutationObserver for dynamic elements
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // ELEMENT_NODE
                        renameButtons(node);
                    }
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

        observer.observe(document.body, { childList: true, subtree: true });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

