
/**
 * Dynamic Subcategory Filtering
 * Handles the dependent dropdown logic for Product Category selection
 */
(function($) {
    $(function() {
        const parentSelect = $('#id_parent_category');
        const subSelect = $('#id_category');

        if (!parentSelect.length || !subSelect.length) return;

        parentSelect.on('change', function() {
            const parentId = $(this).val();
            
            // Clear current subcategories
            subSelect.empty();
            subSelect.append('<option value="">---------</option>');

            if (!parentId) return;

            // Fetch subcategories via AJAX
            $.getJSON(`/products/api/subcategories/${parentId}/`, function(data) {
                $.each(data, function(index, item) {
                    subSelect.append(
                        $('<option></option>').val(item.id).html(item.name)
                    );
                });
            });
        });
    });
})(django.jQuery);
