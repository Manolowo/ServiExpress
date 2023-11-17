// carousel.js
let currentSlide = 0;

function showSlide(index) {
    const carousel = document.querySelector('.carousel');
    const indicators = document.querySelectorAll('.indicator');

    if (index < 0) {
        currentSlide = carousel.children.length - 1;
    } else if (index >= carousel.children.length) {
        currentSlide = 0;
    } else {
        currentSlide = index;
    }

    const translateValue = -currentSlide * 100 + '%';
    carousel.style.transform = 'translateX(' + translateValue + ')';
    
    indicators.forEach((indicator, i) => {
        indicator.classList.toggle('active', i === currentSlide);
    });
}

function nextSlide() {
    showSlide(currentSlide + 1);
}

function prevSlide() {
    showSlide(currentSlide - 1);
}

function goToSlide(index) {
    showSlide(index);
}

// Cambia automáticamente las pestañas cada 5 segundos
setInterval(nextSlide, 5000);
