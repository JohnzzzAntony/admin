(function () {
    'use strict';
    function updateSelectColor(select) {
        const statuses = ['pending', 'packaging', 'ready_for_shipment', 'shipped', 'delivered', 'return_to_origin', 'refund'];
        statuses.forEach(s => select.classList.remove(s));
        select.classList.add(select.value.toLowerCase());
    }
    function init() {
        const selects = document.querySelectorAll('.field-status select');
        selects.forEach(select => {
            updateSelectColor(select);
            select.addEventListener('change', function () { updateSelectColor(this); });
        });
    }
    document.addEventListener('DOMContentLoaded', init);
})();
