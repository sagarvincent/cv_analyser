window.addEventListener('scroll', function() {
    var box = document.querySelector('.container');
    var boxPosition = box.getBoundingClientRect().top;
    var screenPosition = window.innerHeight / 5; // Adjust this value for when you want the effect to trigger

    if (boxPosition < screenPosition) {
        box.classList.add('appear');
    }
});