/**
 * Simplified Permissions Menu System
 * Transforms Django's messy dual-listbox into a clean, grouped menu
 */
(function($) {
    $(function() {
        const selectId = '#id_permissions, #id_user_permissions';
        const $originalSelect = $(selectId);
        
        if (!$originalSelect.length) return;

        console.log('Permission UI: Initializing...');

        // ── 1. Create UI Structure ───────────────────────────────────────────
        const $container = $('<div class="premium-permissions-container"></div>');
        const $menu = $('<div class="perm-menu"></div>');
        const $content = $('<div class="perm-content"></div>');
        
        $container.append($menu).append($content);
        $originalSelect.closest('.form-row').after($container);
        $originalSelect.closest('.form-row').addClass('hidden-perm-row');

        // ── 2. Data Parsing ──────────────────────────────────────────────────
        let permissions = [];
        $originalSelect.find('option').each(function() {
            const val = $(this).val();
            const text = $(this).text(); // e.g., "products | category | Can add category"
            const parts = text.split(' | ');
            
            if (parts.length >= 3) {
                permissions.push({
                    id: val,
                    app: parts[0].trim(),
                    model: parts[1].trim(),
                    action: parts[2].trim(),
                    selected: $(this).prop('selected')
                });
            } else {
                // Handle cases where format is different
                permissions.push({
                    id: val,
                    app: 'Other',
                    model: 'Global',
                    action: text,
                    selected: $(this).prop('selected')
                });
            }
        });

        // Group by App
        const apps = {};
        permissions.forEach(p => {
            if (!apps[p.app]) apps[p.app] = {};
            if (!apps[p.app][p.model]) apps[p.app][p.model] = [];
            apps[p.app][p.model].push(p);
        });

        // ── 3. Rendering ─────────────────────────────────────────────────────
        Object.keys(apps).sort().forEach((appName, index) => {
            // Menu Item
            const $menuItem = $(`<div class="menu-item ${index === 0 ? 'active' : ''}" data-target="app-${index}">
                <i class="fas fa-folder"></i> ${appName}
            </div>`);
            $menu.append($menuItem);

            // App Content
            const $appSection = $(`<div class="app-section ${index === 0 ? 'active' : ''}" id="app-${index}">
                 <h3><i class="fas fa-shield-alt"></i> ${appName} Permissions</h3>
                 <div class="model-cards"></div>
            </div>`);

            Object.keys(apps[appName]).sort().forEach(modelName => {
                const perms = apps[appName][modelName];
                const $card = $(`<div class="model-card">
                    <div class="card-header">
                        <strong>${modelName}</strong>
                        <div class="card-actions">
                            <span class="bulk-toggle" data-action="all">All</span>
                            <span class="bulk-toggle" data-action="none">None</span>
                        </div>
                    </div>
                    <div class="card-body"></div>
                </div>`);

                perms.forEach(p => {
                    const isChecked = $originalSelect.find(`option[value="${p.id}"]`).prop('selected');
                    const $item = $(`<label class="perm-item ${isChecked ? 'checked' : ''}">
                        <input type="checkbox" value="${p.id}" ${isChecked ? 'checked' : ''}>
                        <span>${p.action.replace('Can ', '')}</span>
                    </label>`);
                    $card.find('.card-body').append($item);
                });

                $appSection.find('.model-cards').append($card);
            });

            $content.append($appSection);
        });

        // ── 4. Interactions ──────────────────────────────────────────────────
        // Menu Swapping
        $menu.on('click', '.menu-item', function() {
            const target = $(this).data('target');
            $menu.find('.menu-item').removeClass('active');
            $(this).addClass('active');
            $content.find('.app-section').removeClass('active');
            $(`#${target}`).addClass('active');
        });

        // Sync back to original select
        $container.on('change', 'input[type="checkbox"]', function() {
            const id = $(this).val();
            const checked = $(this).is(':checked');
            
            $originalSelect.find(`option[value="${id}"]`).prop('selected', checked);
            $(this).closest('.perm-item').toggleClass('checked', checked);
            
            // Trigger Django's internal listeners if any
            $originalSelect.trigger('change');
        });

        // Bulk Toggles
        $container.on('click', '.bulk-toggle', function() {
            const action = $(this).data('action');
            const $card = $(this).closest('.model-card');
            const $checkboxes = $card.find('input[type="checkbox"]');
            
            $checkboxes.each(function() {
                const targetState = action === 'all';
                if ($(this).is(':checked') !== targetState) {
                    $(this).prop('checked', targetState).trigger('change');
                }
            });
        });
    });
})(django.jQuery);
