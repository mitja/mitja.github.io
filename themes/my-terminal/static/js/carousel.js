// Carousel functionality for terminal theme
(function() {
  'use strict';

  // Initialize all carousels on the page
  function initCarousels() {
    const carousels = document.querySelectorAll('[data-carousel]');

    carousels.forEach(function(carouselElement) {
      const carouselId = carouselElement.getAttribute('data-carousel');
      const interval = parseInt(carouselElement.getAttribute('data-interval')) || 5000;

      const slides = carouselElement.querySelectorAll('.carousel-slide');
      const indicators = carouselElement.querySelectorAll('.carousel-indicator');
      const prevBtn = carouselElement.querySelector('.carousel-prev');
      const nextBtn = carouselElement.querySelector('.carousel-next');

      let currentSlide = 0;
      let autoplayInterval;
      const totalSlides = slides.length;

      if (totalSlides === 0) return;

      function showSlide(n) {
        // Remove active class from all slides and indicators
        slides.forEach(function(slide) {
          slide.classList.remove('active');
        });
        indicators.forEach(function(indicator) {
          indicator.classList.remove('active');
        });

        // Calculate the current slide index (with wrapping)
        currentSlide = (n + totalSlides) % totalSlides;

        // Add active class to current slide and indicator
        slides[currentSlide].classList.add('active');
        indicators[currentSlide].classList.add('active');
      }

      function nextSlide() {
        showSlide(currentSlide + 1);
        resetAutoplay();
      }

      function prevSlide() {
        showSlide(currentSlide - 1);
        resetAutoplay();
      }

      function goToSlide(n) {
        showSlide(n);
        resetAutoplay();
      }

      function startAutoplay() {
        autoplayInterval = setInterval(function() {
          showSlide(currentSlide + 1);
        }, interval);
      }

      function resetAutoplay() {
        clearInterval(autoplayInterval);
        startAutoplay();
      }

      // Attach event listeners
      if (prevBtn) {
        prevBtn.addEventListener('click', prevSlide);
      }

      if (nextBtn) {
        nextBtn.addEventListener('click', nextSlide);
      }

      indicators.forEach(function(indicator, index) {
        indicator.addEventListener('click', function() {
          goToSlide(index);
        });
      });

      // Start autoplay
      startAutoplay();

      // Pause on hover
      carouselElement.addEventListener('mouseenter', function() {
        clearInterval(autoplayInterval);
      });

      carouselElement.addEventListener('mouseleave', function() {
        startAutoplay();
      });
    });
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCarousels);
  } else {
    initCarousels();
  }
})();
