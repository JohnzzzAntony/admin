
/**
 * Dynamic Subcategory Filtering
 * Handles the dependent dropdown logic for Product Category selection
 */
(function($) {
    $(function() {
        const parentSelect = $('#id_parent_category');
        const subSelect = $('#id_category');

        if (!parentSelect.length || !subSelect.length) {
            console.warn('Category mapping: Could not find selectors #id_parent_category or #id_category');
            return;
        }

        // Listen for change on Parent Category
        parentSelect.on('change', function() {
            const parentId = $(this).val();
            console.log('Category mapping: Parent changed to:', parentId);

            // 1. Reset Sub Category
            subSelect.empty();
            subSelect.append('<option value="">---------</option>');
            
            if (!parentId || parentId === "") {
                subSelect.trigger('change');
                if (subSelect.data('select2')) subSelect.trigger('change.select2');
                return;
            }

            // 2. Add "Loading..." indicator
            subSelect.empty();
            subSelect.append('<option value="">Loading subcategories...</option>');
            if (subSelect.data('select2')) subSelect.trigger('change.select2');

            // 3. Fetch from API
            const apiUrl = `/products/api/subcategories/${parentId}/`;
            $.getJSON(apiUrl, function(data) {
                console.log(`Category mapping: API returned ${data.length} results`);
                
                subSelect.empty();
                subSelect.append('<option value="">---------</option>');
                
                if (data.length === 0) {
                    console.log('Category mapping: No subcategories found for this parent.');
                } else {
                    $.each(data, function(index, item) {
                        subSelect.append(
                            $('<option></option>').val(item.id).html(item.name)
                        );
                    });
                }
                
                // 4. Force UI Refresh for Select2 compatibility
                subSelect.trigger('change');
                if (subSelect.data('select2')) {
                    subSelect.trigger('change.select2');
                }
            }).fail(function(jq) {
                console.error('Category mapping: API Error', jq.responseText);
                subSelect.empty();
                subSelect.append('<option value="">Error loading items</option>');
                if (subSelect.data('select2')) subSelect.trigger('change.select2');
            });
        });
    });
})(django.jQuery);
