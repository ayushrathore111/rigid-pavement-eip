document.getElementById('predictor-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('result').textContent = result.prediction_text;
            document.getElementById('result-popup').style.display = 'flex';
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

document.getElementById('result-popup').addEventListener('click', function(e) {
    if (e.target === this) {
        this.style.display = 'none';
    }
});