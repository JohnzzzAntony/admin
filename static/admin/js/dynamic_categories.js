/**
 * Dynamic Subcategory Filtering
 * Handles the dependent dropdown logic for Product Category selection.
 * When a parent is chosen → API fetches only its subcategories → sub dropdown updates.
 */
(function($) {
    $(function() {
        const parentSelect = $('#id_parent_category');
        const subSelect    = $('#id_category');

        if (!parentSelect.length || !subSelect.length) {
            console.warn('[DynCat] Could not find #id_parent_category or #id_category');
            return;
        }

        // ── Helpers ──────────────────────────────────────────────────────────

        function setSubLabel(text, isError) {
            subSelect.empty().append(
                $('<option>').val('').text(text)
            );
            if (subSelect.data('select2')) subSelect.trigger('change.select2');
        }

        function showLoading() {
            setSubLabel('Loading subcategories…');
        }

        function populateSubs(data) {
            subSelect.empty().append($('<option>').val('').text('---------'));
            if (data.length === 0) {
                subSelect.append($('<option>').val('').text('No subcategories (products assigned directly)').prop('disabled', true));
            } else {
                $.each(data, function(_, item) {
                    subSelect.append($('<option>').val(item.id).text(item.name));
                });
            }
            if (subSelect.data('select2')) subSelect.trigger('change.select2');
        }

        function fetchSubs(parentId) {
            if (!parentId) {
                setSubLabel('---------');
                return;
            }
            showLoading();
            $.getJSON('/products/api/subcategories/' + parentId + '/', function(data) {
                console.log('[DynCat] Received', data.length, 'subcategories for parent', parentId);
                populateSubs(data);
            }).fail(function(jqXHR) {
                console.error('[DynCat] API Error', jqXHR.status, jqXHR.responseText);
                setSubLabel('Error loading – try refreshing', true);
            });
        }

        // ── Init ─────────────────────────────────────────────────────────────

        // On page load, if a parent is already set (edit mode), fetch its subs
        const currentParentId = parentSelect.val();
        if (currentParentId) {
            // Fetch subs, then re-select the previously saved category
            const savedCategoryId = subSelect.val();
            fetchSubs(currentParentId);
            // After fetch completes, re-select the saved sub
            setTimeout(function() {
                if (savedCategoryId) {
                    subSelect.val(savedCategoryId);
                    if (subSelect.data('select2')) subSelect.trigger('change.select2');
                }
            }, 1500);
        }

        // ── Events ────────────────────────────────────────────────────────────
        parentSelect.on('change', function() {
            const parentId = $(this).val();
            console.log('[DynCat] Parent changed to:', parentId);
            fetchSubs(parentId);
        });
    });
})(django.jQuery);
