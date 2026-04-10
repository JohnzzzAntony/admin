
function togglePermissionApp(id) {
    const content = document.getElementById('section-' + id);
    if (!content) return;
    
    const header = content.previousElementSibling;
    const icon = header.querySelector('.fa-chevron-down');
    
    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        if (icon) icon.style.transform = 'rotate(180deg)';
    } else {
        content.classList.add('hidden');
        if (icon) icon.style.transform = 'rotate(0deg)';
    }
}
