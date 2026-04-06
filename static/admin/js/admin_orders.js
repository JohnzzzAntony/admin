
document.addEventListener('DOMContentLoaded', function() {
    // Function to update select coloring based on value
    const updateSelectColor = (select) => {
        select.setAttribute('data-status', select.value);
    };

    // Initial coloring for all status selects in the list view
    const statusSelects = document.querySelectorAll('.field-status select');
    statusSelects.forEach(select => {
        updateSelectColor(select);
        select.addEventListener('change', () => updateSelectColor(select));
    });
});
