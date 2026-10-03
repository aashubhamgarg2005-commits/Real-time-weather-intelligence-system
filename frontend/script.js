// =========================
// District Weather Data
// =========================

const weatherData = {
    Meerut: {
        temperature: 28,
        condition: "Light Rain",
        humidity: 82,
        windSpeed: "12 km/h",
        pressure: "1008 hPa",
        rainfall: "2.4 mm",
        prediction: 78,
        alert: "Moderate chance of rain in the next few hours.",
        forecast: [
            { time: "2 PM", temp: "28°C", rain: 70 },
            { time: "3 PM", temp: "27°C", rain: 80 },
            { time: "4 PM", temp: "26°C", rain: 85 },
            { time: "5 PM", temp: "25°C", rain: 75 },
            { time: "6 PM", temp: "25°C", rain: 60 }
        ]
    },

    Ghaziabad: {
        temperature: 30,
        condition: "Cloudy",
        humidity: 75,
        windSpeed: "10 km/h",
        pressure: "1010 hPa",
        rainfall: "0.8 mm",
        prediction: 55,
        alert: "Moderate possibility of rain.",
        forecast: [
            { time: "2 PM", temp: "30°C", rain: 40 },
            { time: "3 PM", temp: "29°C", rain: 50 },
            { time: "4 PM", temp: "28°C", rain: 60 },
            { time: "5 PM", temp: "27°C", rain: 55 },
            { time: "6 PM", temp: "26°C", rain: 45 }
        ]
    },

    Noida: {
        temperature: 31,
        condition: "Partly Cloudy",
        humidity: 68,
        windSpeed: "14 km/h",
        pressure: "1009 hPa",
        rainfall: "0.0 mm",
        prediction: 35,
        alert: "Low chance of rain in the next few hours.",
        forecast: [
            { time: "2 PM", temp: "31°C", rain: 25 },
            { time: "3 PM", temp: "30°C", rain: 30 },
            { time: "4 PM", temp: "29°C", rain: 40 },
            { time: "5 PM", temp: "28°C", rain: 35 },
            { time: "6 PM", temp: "27°C", rain: 30 }
        ]
    },

    Lucknow: {
        temperature: 29,
        condition: "Rain",
        humidity: 88,
        windSpeed: "16 km/h",
        pressure: "1005 hPa",
        rainfall: "5.2 mm",
        prediction: 88,
        alert: "High probability of rain. Stay alert.",
        forecast: [
            { time: "2 PM", temp: "29°C", rain: 85 },
            { time: "3 PM", temp: "28°C", rain: 90 },
            { time: "4 PM", temp: "27°C", rain: 88 },
            { time: "5 PM", temp: "26°C", rain: 80 },
            { time: "6 PM", temp: "26°C", rain: 70 }
        ]
    },

    Agra: {
        temperature: 33,
        condition: "Sunny",
        humidity: 52,
        windSpeed: "9 km/h",
        pressure: "1012 hPa",
        rainfall: "0.0 mm",
        prediction: 15,
        alert: "No significant rain expected.",
        forecast: [
            { time: "2 PM", temp: "33°C", rain: 10 },
            { time: "3 PM", temp: "32°C", rain: 15 },
            { time: "4 PM", temp: "31°C", rain: 20 },
            { time: "5 PM", temp: "30°C", rain: 18 },
            { time: "6 PM", temp: "29°C", rain: 12 }
        ]
    },

    Kanpur: {
        temperature: 30,
        condition: "Cloudy",
        humidity: 78,
        windSpeed: "13 km/h",
        pressure: "1007 hPa",
        rainfall: "1.2 mm",
        prediction: 65,
        alert: "High chance of rain in the next few hours.",
        forecast: [
            { time: "2 PM", temp: "30°C", rain: 60 },
            { time: "3 PM", temp: "29°C", rain: 70 },
            { time: "4 PM", temp: "28°C", rain: 72 },
            { time: "5 PM", temp: "27°C", rain: 65 },
            { time: "6 PM", temp: "27°C", rain: 55 }
        ]
    },

    Varanasi: {
        temperature: 27,
        condition: "Heavy Rain",
        humidity: 92,
        windSpeed: "20 km/h",
        pressure: "1003 hPa",
        rainfall: "8.5 mm",
        prediction: 92,
        alert: "Severe rain probability. Please stay alert.",
        forecast: [
            { time: "2 PM", temp: "27°C", rain: 90 },
            { time: "3 PM", temp: "26°C", rain: 95 },
            { time: "4 PM", temp: "25°C", rain: 92 },
            { time: "5 PM", temp: "25°C", rain: 85 },
            { time: "6 PM", temp: "24°C", rain: 75 }
        ]
    }
};


// =========================
// Update Weather UI
// =========================

function updateWeather(district) {

    const data = weatherData[district];

    document.getElementById("temperature").textContent =
        data.temperature;

    document.getElementById("condition").textContent =
        data.condition;

    document.getElementById("districtName").textContent =
        district;

    document.getElementById("humidity").textContent =
        data.humidity + "%";

    document.getElementById("windSpeed").textContent =
        data.windSpeed;

    document.getElementById("pressure").textContent =
        data.pressure;

    document.getElementById("rainfall").textContent =
        data.rainfall;

    document.getElementById("mlPrediction").textContent =
        data.prediction;

    document.getElementById("alertMessage").textContent =
        data.alert;

    updateForecast(data.forecast);
    updateLastUpdated();
}


// =========================
// Update Forecast Cards
// =========================

function updateForecast(forecast) {

    const container =
        document.getElementById("forecastContainer");

    container.innerHTML = "";

    forecast.forEach(item => {

        container.innerHTML += `
            <div class="col-6 col-md">

                <div class="forecast-card text-center">

                    <h6>${item.time}</h6>

                    <i class="bi bi-cloud-rain-fill"></i>

                    <h5>${item.temp}</h5>

                    <span>${item.rain}% 🌧️</span>

                </div>

            </div>
        `;
    });
}


// =========================
// District Button Click
// =========================

const districtButtons =
    document.querySelectorAll(".district-btn");

districtButtons.forEach(button => {

    button.addEventListener("click", function () {

        // Remove active class
        districtButtons.forEach(btn =>
            btn.classList.remove("active")
        );

        // Add active class
        this.classList.add("active");

        // Get district name
        const district = this.textContent.trim();

        // Update UI
        updateWeather(district);
    });

});


// =========================
// Last Updated Time
// =========================

function updateLastUpdated() {

    const now = new Date();

    document.getElementById("lastUpdated").textContent =
        now.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
        });
}


// =========================
// Initial Load
// =========================

updateLastUpdated();