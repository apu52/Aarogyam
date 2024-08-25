function countUp(element, start, end, duration) {
    let current = start;
    const range = end - start;
    const increment = end > start ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    const obj = document.getElementById(element);
    const timer = setInterval(function() {
        current += increment;
        obj.textContent = current + "+";
        if (current == end) {
            clearInterval(timer);
        }
    }, stepTime);
}

// Count up for each number
window.onload = function() {
    countUp("psychologists-count", 0, 190, 2000);
    countUp("psychiatrists-count", 0, 100, 2000);
    countUp("counselors-count", 0, 300, 2000);
    countUp("neuropsychologists-count", 0, 120, 2000);
};

