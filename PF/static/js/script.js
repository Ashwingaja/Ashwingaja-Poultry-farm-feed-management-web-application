document.getElementById("prediction-form").addEventListener("submit", function (e) {
    e.preventDefault();

    const startAge = parseFloat(document.getElementById("start_age").value);
    const endAge = parseFloat(document.getElementById("end_age").value);
    const birdCount = parseInt(document.getElementById("bird_count").value);
    const fcr = parseFloat(document.getElementById("fcr").value);
    const feedCost = parseFloat(document.getElementById("feed_cost").value);

    // Clear previous result
    document.getElementById("predictions").innerHTML = "";
    document.getElementById("total-cost").innerHTML = "";
    document.getElementById("error-message").style.display = "none";

    // Validate inputs
    if (isNaN(startAge) || isNaN(endAge) || isNaN(birdCount) || isNaN(fcr) || isNaN(feedCost)) {
        document.getElementById("error-message").textContent = "Please enter valid numbers for all fields.";
        document.getElementById("error-message").style.display = "block";
        return;
    }

    // Make the prediction request to Flask backend
    fetch('/predict', {
        method: 'POST',
        body: new URLSearchParams({
            start_age: startAge,
            end_age: endAge,
            bird_count: birdCount,
            fcr: fcr,
            feed_cost: feedCost
        }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("error-message").textContent = data.error;
            document.getElementById("error-message").style.display = "block";
        } else {
            const predictions = data.predictions;
            let predictionsHTML = "<h3>Predicted Daily Feed for Each Age:</h3><ul>";
            for (const age in predictions) {
                predictionsHTML += `<li>Age ${age}: ${predictions[age].toFixed(2)} kg</li>`;
            }
            predictionsHTML += "</ul>";

            const totalCost = data.total_cost.toFixed(2);
            document.getElementById("predictions").innerHTML = predictionsHTML;
            document.getElementById("total-cost").innerHTML = `Total Feed Cost: ₹${totalCost}`;

            document.getElementById("result").style.display = "block";
        }
    })
    .catch(error => {
        document.getElementById("error-message").textContent = "An error occurred. Please try again.";
        document.getElementById("error-message").style.display = "block";
    });
});
