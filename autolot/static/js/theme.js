document.addEventListener('DOMContentLoaded', () => {
    const storageKey = 'theme-preference';
    const body = document.body;
    const toggleButton = document.getElementById('theme-toggle');

    function getInitialTheme() {
        const saved = localStorage.getItem(storageKey);
        if (saved === 'light' || saved === 'dark') {
            return saved;
        }
        const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
        return prefersLight ? 'light' : 'dark';
    }

    function setToggleIcon(theme) {
        if (!toggleButton) return;
        const isLight = theme === 'light';
        toggleButton.textContent = isLight ? '🌙' : '☀️';
        toggleButton.setAttribute(
            'aria-label',
            isLight ? 'Switch to dark mode' : 'Switch to light mode'
        );
    }

    function applyTheme(theme, { persist = true } = {}) {
        if (theme === 'light') {
            body.classList.add('light-mode');
        } else {
            body.classList.remove('light-mode');
        }
        if (persist) {
            localStorage.setItem(storageKey, theme);
        }
        setToggleIcon(theme);
    }

    const initialTheme = getInitialTheme();
    applyTheme(initialTheme, { persist: false });

    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            const current = body.classList.contains('light-mode') ? 'light' : 'dark';
            const next = current === 'light' ? 'dark' : 'light';
            applyTheme(next);
        });
    }

    /* --------------- INVENTORY IMAGE CAROUSEL --------------- */

    function cycleImage(event, direction) {
        event.preventDefault();
        event.stopPropagation();

        const container = event.currentTarget.closest('.card-image-container');
        if (!container) return;

        const img = container.querySelector('.card-car-img');
        if (!img) return;

        const urlsString = img.dataset.photoUrls || img.getAttribute('data-photo-urls');
        if (!urlsString) return;

        const photoUrls = urlsString.split('|').filter(Boolean);
        if (!photoUrls.length) return;

        const totalPhotos = photoUrls.length;
        let currentIndex = parseInt(img.dataset.currentIndex || '0', 10) || 0;

        let nextIndex = currentIndex;
        if (direction === 'next') {
            nextIndex = (currentIndex + 1) % totalPhotos;
        } else if (direction === 'prev') {
            nextIndex = (currentIndex - 1 + totalPhotos) % totalPhotos;
        } else {
            return;
        }

        img.style.opacity = '0';

        setTimeout(() => {
            img.src = photoUrls[nextIndex];
            img.dataset.currentIndex = String(nextIndex);
            img.style.opacity = '1';
        }, 300);
    }

    document.querySelectorAll('.card-next-btn').forEach(button => {
        button.addEventListener('click', (event) => cycleImage(event, 'next'));
    });

    document.querySelectorAll('.card-back-btn').forEach(button => {
        button.addEventListener('click', (event) => cycleImage(event, 'prev'));
    });
});

(function () {
    const menuToggle = document.getElementById('nav-mobile-toggle');
    const navList = document.getElementById('primary-nav');

    if (!menuToggle || !navList) return;

    menuToggle.addEventListener('click', () => {
        const isOpen = navList.classList.toggle('nav-open');
        menuToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
})();
