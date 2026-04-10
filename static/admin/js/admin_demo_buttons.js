/**
 * Admin Demo Buttons Injection
 * Injects "Demo Excel" and "Demo CSV" buttons into the Product list header.
 */
(function($) {
    $(function() {
        // Target the Import/Export button group
        // Jazzmin usually places these in .card-header or near #searchbar
        const exportLink = $('.export_link');
        
        if (exportLink.length) {
            // Generate full URLs using the relative path from the current changelist URL
            // Current URL is typically /admin/products/product/
            const excelUrl = 'download-demo-excel/';
            const csvUrl = 'download-demo-csv/';

            console.log('[DemoButtons] Injecting demo download links...');

            // Create buttons with Jazzmin/Bootstrap styles
            const excelBtn = $('<a href="' + excelUrl + '" class="btn btn-outline-info btn-sm mr-2 ml-2" style="font-weight:600; border-radius:30px; box-shadow:0 2px 4px rgba(0,0,0,0.05);">' + 
                               '<i class="fas fa-download mr-1"></i> Demo Excel (.xlsx)</a>');
            
            const csvBtn = $('<a href="' + csvUrl + '" class="btn btn-outline-info btn-sm mr-2" style="font-weight:600; border-radius:30px; box-shadow:0 2px 4px rgba(0,0,0,0.05);">' + 
                             '<i class="fas fa-download mr-1"></i> Demo CSV (.csv)</a>');

            // Insert after the Export button
            exportLink.after(csvBtn).after(excelBtn);
        }
    });
})(window.jQuery || window.django.jQuery);
