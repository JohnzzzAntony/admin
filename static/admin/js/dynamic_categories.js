/**
 * Dynamic Subcategory Filtering (Hardened Version)
 * Handles the dependent dropdown logic for Product Category selection.
 * When a parent is chosen → API fetches only its subcategories → sub dropdown updates.
 */
(function() {
    // Wait for Django's jQuery to be available
    const init = function($) {
        $(function() {
            const parentSelect = $('#id_parent_category');
            const subSelect    = $('#id_category');

            if (!parentSelect.length || !subSelect.length) {
                return;
            }

            function setSubLabel(text) {
                subSelect.empty().append($('<option>').val('').text(text));
                if (subSelect.data('select2')) subSelect.trigger('change.select2');
            }

            function populateSubs(data, savedId = null) {
                subSelect.empty().append($('<option>').val('').text('---------'));
                if (data && data.length > 0) {
                    $.each(data, function(_, item) {
                        subSelect.append($('<option>').val(item.id).text(item.name));
                    });
                    
                    if (savedId) {
                        subSelect.val(savedId);
                    }
                } else {
                    subSelect.append($('<option>').val('').text('No subcategories found').prop('disabled', true));
                }
                
                if (subSelect.data('select2')) {
                    subSelect.trigger('change.select2');
                }
            }

            function fetchSubs(parentId, savedId = null) {
                if (!parentId) {
                    setSubLabel('---------');
                    return;
                }

                setSubLabel('Loading subcategories...');
                
                $.ajax({
                    url: '/products/api/subcategories/' + parentId + '/',
                    type: 'GET',
                    dataType: 'json',
                    success: function(data) {
                        populateSubs(data, savedId);
                    },
                    error: function() {
                        setSubLabel('Error loading subcategories');
                    }
                });
            }

            const initialParent = parentSelect.val();
            const initialSub    = subSelect.val();

            if (initialParent) {
                fetchSubs(initialParent, initialSub);
            }

            parentSelect.on('change', function() {
                fetchSubs($(this).val());
            });
        });
    };

    // Check for jQuery in multiple possible places (Django Admin vs Standalone)
    if (typeof django !== 'undefined' && django.jQuery) {
        init(django.jQuery);
    } else if (typeof jQuery !== 'undefined') {
        init(jQuery);
    } else {
        // Fallback for late-loading scripts
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof django !== 'undefined' && django.jQuery) {
                init(django.jQuery);
            } else if (typeof jQuery !== 'undefined') {
                init(jQuery);
            }
        });
    }
})();

