window.addEventListener('scroll', function() {
    var background = document.querySelector('.background');
    var scrollPosition = window.scrollY;

    if (scrollPosition > 100) { // Adjust the value as needed
        background.style.display = 'none'; // Hide the background after scrolling
    }
});
