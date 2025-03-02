new Typed('#typed', {
    strings: [
        "Welcome to Fake Review Detection!",
        "We check for: ",
        "✓ Spam-like content",
        "✓ Sentiment manipulation",
        "✓ Repeated patterns",
        "✓ Unrealistic timelines",
        "Submit your review to check!"
    ],
    typeSpeed: 50,
    backSpeed: 25,
    loop: true
});

const form = document.getElementById('reviewForm');
const resultDiv = document.getElementById('result');

form.addEventListener('submit', function(event) {
    event.preventDefault();
    submitReview();
});

function submitReview() {
    const formData = new FormData(form);

    axios.post('/predict', formData)
        .then(response => {
            const data = response.data;
            resultDiv.innerHTML = `
                <p><b>User ID:</b> ${data.user_id}</p>
                <p><b>Product ID:</b> ${data.product_id}</p>
                <p><b>Review:</b> ${data.review}</p>
                <p><b>Purchase Verified:</b> ${data.purchase_verified}</p>
                <p><b>Prediction:</b> ${data.prediction}</p>
                <p><b>Proof:</b> ${data.proof}</p>
                <p><b>Timestamp:</b> ${new Date(data.timestamp * 1000).toLocaleString()}</p>
                <p><b>Hash:</b> ${data.hash}</p>
            `;
        })
        .catch(error => {
            console.error('There was an error!', error);
        });
}

function fetchReviews() {
    fetch("/review-chain")
    .then(response => response.json())
    .then(reviews => {
        console.log("Fetched reviews:", reviews); // Log fetched reviews
        let reviewTable = $("#reviewList");
        reviewTable.html(reviews.map(review => `
            <tr style="color: ${review.prediction === 'Genuine Review' ? 'green' : 'red'}">
                <td>${review.user_id}</td>
                <td>${review.product_id}</td>
                <td>${review.review}</td>
                <td>${review.prediction}</td>
            </tr>
        `).join(""));
    })
    .catch(error => console.error("Error:", error));
}

$(document).ready(() => {
    fetchReviews();
});
