
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
            console.log('Parent category changed:', parentId);
            
            // Clear current subcategories
            subSelect.empty();
            subSelect.append('<option value="">---------</option>');

            if (!parentId) {
                subSelect.trigger('change');
                if (subSelect.data('select2')) subSelect.trigger('change.select2');
                return;
            }

            // Fetch subcategories via AJAX
            const apiUrl = `/products/api/subcategories/${parentId}/`;
            console.log('Fetching subcategories from:', apiUrl);

            $.getJSON(apiUrl, function(data) {
                console.log('Subcategories received:', data);
                $.each(data, function(index, item) {
                    subSelect.append(
                        $('<option></option>').val(item.id).html(item.name)
                    );
                });
                // Updated for Select2 compatibility
                subSelect.trigger('change');
                if (subSelect.data('select2')) {
                    subSelect.trigger('change.select2');
                }
            }).fail(function(jqXHR, textStatus, errorThrown) {
                console.error('API Error:', textStatus, errorThrown);
            });
        });
    });
})(django.jQuery);
