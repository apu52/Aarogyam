<script>
document.getElementById('quiz-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    // Convert all values to numbers
    for (let key in data) {
        data[key] = Number(data[key]);
    }

    try {
        const response = await fetch('http://your-backend-url/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        alert('Prediction: ' + result.prediction);
    } catch (error) {
        console.error('Error:', error);
    }
});
</script>
