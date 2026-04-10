/**
 * Admin Demo Buttons Injection
 * Injects "Demo Excel" and "Demo CSV" buttons into the Product list header.
 */
(function($) {
    $(function() {
        // Target the Import/Export button group
        // Jazzmin usually places these in .card-header or near #searchbar
        const exportLink = $('.export_link');
        
        if (exportLink.length && !$('#export-dropdown-wrapper').length) {
            const originalHref = exportLink.attr('href');
            console.log('[DemoButtons] Transforming Export button into dropdown...');

            // Create dropdown wrapper with original export link as the first item
            const dropdownHtml = `
                <div class="dropdown d-inline-block mr-2" id="export-dropdown-wrapper">
                    <button class="btn btn-secondary dropdown-toggle font-weight-bold" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false" style="border-radius:30px; padding: 0.375rem 1.25rem;">
                        <i class="fas fa-download mr-1"></i> EXPORT
                    </button>
                    <div class="dropdown-menu shadow border-0" style="border-radius: 12px; min-width: 220px; margin-top: 10px;">
                        <div class="dropdown-header font-weight-bold text-dark text-uppercase small" style="letter-spacing: 0.5px;">Actions</div>
                        <a class="dropdown-item py-2" href="${originalHref}">
                            <i class="fas fa-file-export mr-2 text-muted"></i> Export Current List
                        </a>
                        <div class="dropdown-divider"></div>
                        <div class="dropdown-header font-weight-bold text-dark text-uppercase small" style="letter-spacing: 0.5px;">Sample Templates</div>
                        <a class="dropdown-item py-2" href="download-demo-excel/">
                            <i class="fas fa-file-excel mr-2 text-success"></i> Demo Excel (.xlsx)
                        </a>
                        <a class="dropdown-item py-2" href="download-demo-csv/">
                            <i class="fas fa-file-csv mr-2 text-info"></i> Demo CSV (.csv)
                        </a>
                    </div>
                </div>
            `;

            // Replace the original export link with the new dropdown
            exportLink.replaceWith(dropdownHtml);
        }
    });
})(window.jQuery || window.django.jQuery);
