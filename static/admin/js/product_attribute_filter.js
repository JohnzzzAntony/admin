(function ($) {
    'use strict';
    $(document).ready(function () {
        // Automatically filters Value Options based on the selected Attribute
        function updateOptions($attributeSelect, selectedOptionId) {
            var attributeId = $attributeSelect.val();
            var $optionSelect = $('#' + $attributeSelect.attr('id').replace('-attribute', '-attribute_option'));

            if (!attributeId) {
                $optionSelect.empty().append('<option value="">---------</option>');
                return;
            }

            // Fetch possibilities for this attribute via the new API
            $.getJSON('/products/api/attribute-options/' + attributeId + '/', function (data) {
                var currentVal = selectedOptionId || $optionSelect.val();
                $optionSelect.empty().append('<option value="">---------</option>');
                $.each(data, function (index, opt) {
                    var isSelected = (opt.id == currentVal);
                    $optionSelect.append($('<option></option>').val(opt.id).text(opt.value).prop('selected', isSelected));
                });
            });
        }

        // Handle changes in the Attribute dropdown
        $(document).on('change', 'select[id^="id_characteristics-"][id$="-attribute"]', function () {
            updateOptions($(this));
        });

        // Initialize rows on page load
        $('select[id^="id_characteristics-"][id$="-attribute"]').each(function () {
            var $this = $(this);
            if ($this.val()) {
                var $optInput = $('#' + $this.attr('id').replace('-attribute', '-attribute_option'));
                updateOptions($this, $optInput.val());
            }
        });
    });
})(django.jQuery);
