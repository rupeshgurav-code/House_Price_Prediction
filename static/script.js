const form = document.getElementById("predictForm");
const result = document.getElementById("result");
const btn = document.getElementById("predictBtn");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    result.classList.add("loading");
    result.innerHTML = "Predicting price...";

    btn.disabled = true;
    btn.innerHTML = "Processing...";

    const formData = new FormData(form);

    try {
        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            result.classList.remove("loading");
            result.innerHTML = `🏠 Estimated Price: ₹ ${data.prediction}`;
        } else {
            result.classList.remove("loading");
            result.innerHTML = `❌ ${data.error}`;
        }

    } catch (err) {
        result.innerHTML = "❌ Server Error";
    }

    btn.disabled = false;
    btn.innerHTML = "🔮 Predict Price";
});