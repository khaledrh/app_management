document.addEventListener("DOMContentLoaded", function() {
    const results = document.querySelectorAll('.result-item');
    let currentIndex = 0;

    function showSlide(index) {
        results.forEach((item, i) => {
            item.classList.remove('active'); // Hide all slides
            if (i === index) {
                item.classList.add('active'); // Show only active slide
            }
        });
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % results.length; // Loop back to first slide
        showSlide(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + results.length) % results.length; // Loop back to last slide
        showSlide(currentIndex);
    }

    // Initial setup
    showSlide(currentIndex);

    // Show all items and hide controls for large screens
    if (window.innerWidth > 768) {
        results.forEach(item => item.classList.remove('inactive')); // Show all items
        document.querySelector('.slideshow-controls').style.display = 'none';
    }

    // Add event listeners for buttons
    window.prevSlide = prevSlide;
    window.nextSlide = nextSlide;

    // Recheck on window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            results.forEach(item => item.classList.remove('inactive')); // Show all items
            document.querySelector('.slideshow-controls').style.display = 'none'; // Hide controls
        } else {
            showSlide(currentIndex); // Reset slideshow for small screens
            document.querySelector('.slideshow-controls').style.display = 'flex'; // Show controls
        }
    });
});