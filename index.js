document.addEventListener("DOMContentLoaded", function () {
    const counters = document.querySelectorAll('.data-lists h1');
    const speed = 200; // The lower the speed, the faster the count
  
    counters.forEach(counter => {
      const updateCount = () => {
        const target = +counter.getAttribute('data-target');
        const count = +counter.innerText;
  
        // Lower increment to slow down the counting
        const increment = target / speed;
  
        if (count < target) {
          counter.innerText = Math.ceil(count + increment);
          setTimeout(updateCount, 10);
        } else {
          counter.innerText = target;
        }
      };
  
      updateCount();
    });
  });
  