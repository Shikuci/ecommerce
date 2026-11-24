(function () {
    const root = document.documentElement;
    const button = document.getElementById('theme-toggle');
    const icon = document.getElementById('theme-toggle-icon');

    if (!button || !icon) return;

    function applyTheme(theme, persist) {
        const isDark = theme === 'dark';
        root.setAttribute('data-theme', isDark ? 'dark' : 'light');
        icon.className = isDark ? 'fas fa-moon' : 'fas fa-sun';
        button.setAttribute('aria-label', isDark ? 'Switch to light mode' : 'Switch to dark mode');
        button.setAttribute('title', isDark ? 'Light mode' : 'Dark mode');
        button.setAttribute('aria-pressed', isDark ? 'true' : 'false');

        if (persist) {
            try {
                localStorage.setItem('ecom-theme', isDark ? 'dark' : 'light');
            } catch (error) {
                // The selected theme still applies for the current page.
            }
        }
    }

    let savedTheme = 'light';
    try {
        savedTheme = localStorage.getItem('ecom-theme') === 'dark' ? 'dark' : 'light';
    } catch (error) {
        savedTheme = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    }
    applyTheme(savedTheme, false);

    button.addEventListener('click', function () {
        applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark', true);
    });
}());
