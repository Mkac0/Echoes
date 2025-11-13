document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');
    const body = document.body;
    const storageKey = 'theme-preference';

    function applyTheme(theme) {
        if (theme === 'light') {
            body.classList.add('light-mode');
            toggleButton.textContent = 'Switch to Dark Mode';
        } else {
            body.classList.remove('light-mode');
            toggleButton.textContent = 'Switch to Light Mode';
        }
        localStorage.setItem(storageKey, theme);
    }
    const savedTheme = localStorage.getItem(storageKey);

    if (savedTheme) {
        applyTheme(savedTheme);
    } else {
        const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
        if (prefersLight) {
            applyTheme('light');
        } else {
            applyTheme('dark');
        }
    }
    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            const currentTheme = body.classList.contains('light-mode') ? 'light' : 'dark';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }
});

function cycleImage(event, direction) {
    event.preventDefault();
    event.stopPropagation();

    const container = event.target.closest('.card-image-container');
    const img = container.querySelector('.card-car-img');
    
    const urlsString = img.getAttribute('data-photo-urls');
    if (!urlsString) return;

    const photoUrls = urlsString.split('|');
    const totalPhotos = photoUrls.length;
    let currentIndex = parseInt(img.getAttribute('data-current-index') || '0', 10);
    
    let nextIndex;

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
        img.setAttribute('data-current-index', nextIndex);
        img.style.opacity = '1';
    }, 300);
}

document.querySelectorAll('.card-next-btn').forEach(button => {
    button.addEventListener('click', (event) => cycleImage(event, 'next'));
});

document.querySelectorAll('.card-back-btn').forEach(button => {
    button.addEventListener('click', (event) => cycleImage(event, 'prev'));
});
