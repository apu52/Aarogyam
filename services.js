document.addEventListener('DOMContentLoaded', () => {
    // Function to animate the count
    function animateCountUp(element, start, end, duration) {
        let startTime = null;
        const step = (currentTime) => {
            if (!startTime) startTime = currentTime;
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const currentCount = Math.floor(progress * (end - start) + start);
            element.textContent = currentCount;
            if (progress < 1) {
                requestAnimationFrame(step);
            }
        };
        requestAnimationFrame(step);
    }

    // Select all elements with data-count
    const countElements = document.querySelectorAll('.data-lists h1');

    // Observer to trigger the count up when the element is in view
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const endValue = parseInt(element.textContent, 10);
                animateCountUp(element, 0, endValue, 2000); // 2000ms = 2s duration
                observer.unobserve(element); // Stop observing after the animation has started
            }
        });
    }, { threshold: 0.5 });

    // Observe each count element
    countElements.forEach(element => {
        observer.observe(element);
    });
});
