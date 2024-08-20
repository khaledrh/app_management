function setFontSize(size) {
    document.documentElement.style.fontSize = size;
    localStorage.setItem('fontSize', size); // Save user preference
}

// Function to toggle high contrast mode
function toggleContrast() {
    document.body.classList.toggle('high-contrast');
    const isHighContrast = document.body.classList.contains('high-contrast');
    localStorage.setItem('highContrast', isHighContrast ? 'enabled' : 'disabled');
}

// Function to confirm account deletion
function confirmDelete() {
    return confirm("Are you sure you want to delete your account? This action cannot be undone.");
}

// On page load, apply saved settings
document.addEventListener('DOMContentLoaded', function() {
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        document.documentElement.style.fontSize = savedFontSize;
    }

    const highContrast = localStorage.getItem('highContrast');
    if (highContrast === 'enabled') {
        document.body.classList.add('high-contrast');
    }
});