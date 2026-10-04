// =========================
// API Configuration
// =========================

const API_BASE_URL = "http://127.0.0.1:8000";

let selectedDistrict = "meerut";


// =========================
// Update Weather UI
// =========================

function updateWeather(data) {

    document.getElementById("temperature").textContent =
        formatNumber(data.temperature_2m);

    document.getElementById("condition").textContent =
        getWeatherCondition(data);

    document.getElementById("districtName").textContent =
        capitalize(data.district);

    document.getElementById("humidity").textContent =
        formatNumber(data.relative_humidity_2m) + "%";

    document.getElementById("windSpeed").textContent =
        formatNumber(data.wind_speed_10m) + " km/h";

    document.getElementById("pressure").textContent =
        formatNumber(data.pressure_msl) + " hPa";

    document.getElementById("rainfall").textContent =
        formatNumber(data.precipitation) + " mm";

    updateRainAlert(data);

    updateLastUpdated(data.time);
}


// =========================
// Fetch Weather From Backend
// =========================

async function fetchWeather(district) {

    try {

        console.log(
            `Fetching weather for ${district}...`
        );

        const response = await fetch(
            `${API_BASE_URL}/api/weather/${district}`
        );

        if (!response.ok) {

            throw new Error(
                `HTTP ${response.status}`
            );
        }

        const data = await response.json();

        console.log("Weather data:", data);

        updateWeather(data);

    } catch (error) {

        console.error(
            "Failed to fetch weather:",
            error
        );

        document.getElementById("condition").textContent =
            "Unable to fetch weather";

        document.getElementById("alertMessage").textContent =
            "Unable to connect to the weather server.";
    }
}


// =========================
// Weather Condition
// =========================

function getWeatherCondition(data) {

    const precipitation =
        Number(data.precipitation || 0);

    const rain =
        Number(data.rain || 0);

    const showers =
        Number(data.showers || 0);

    const cloudCover =
        Number(data.cloud_cover || 0);


    if (rain > 0 || showers > 0) {

        if (rain >= 5) {
            return "Heavy Rain";
        }

        return "Rain";
    }


    if (precipitation > 0) {
        return "Light Rain";
    }


    if (cloudCover >= 75) {
        return "Cloudy";
    }


    if (cloudCover >= 40) {
        return "Partly Cloudy";
    }


    return "Clear Sky";
}


// =========================
// Rain Alert
// =========================

function updateRainAlert(data) {

    const precipitation =
        Number(data.precipitation || 0);

    const rain =
        Number(data.rain || 0);

    const showers =
        Number(data.showers || 0);


    if (
        precipitation > 0 ||
        rain > 0 ||
        showers > 0
    ) {

        document.getElementById("alertMessage").textContent =
            "Rain is currently being detected in this district.";

    } else {

        document.getElementById("alertMessage").textContent =
            "No rainfall is currently being detected.";
    }
}


// =========================
// District Button Click
// =========================

const districtButtons =
    document.querySelectorAll(".district-btn");


districtButtons.forEach(button => {

    button.addEventListener("click", function () {

        // Remove active class
        districtButtons.forEach(btn => {
            btn.classList.remove("active");
        });


        // Add active class
        this.classList.add("active");


        // Get district name
        selectedDistrict =
            this.textContent.trim().toLowerCase();


        console.log(
            `Selected district: ${selectedDistrict}`
        );


        // Fetch live weather
        fetchWeather(selectedDistrict);
    });

});


// =========================
// Last Updated Time
// =========================

function updateLastUpdated(time) {

    if (!time) {

        document.getElementById("lastUpdated").textContent =
            "--:--";

        return;
    }


    const date = new Date(time);


    document.getElementById("lastUpdated").textContent =
        date.toLocaleTimeString("en-IN", {
            hour: "2-digit",
            minute: "2-digit"
        });
}


// =========================
// Format Number
// =========================

function formatNumber(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "--";
    }


    const number = Number(value);


    if (Number.isNaN(number)) {
        return "--";
    }


    return number.toFixed(1);
}


// =========================
// Capitalize District
// =========================

function capitalize(text) {

    if (!text) {
        return "--";
    }


    return text.charAt(0).toUpperCase() +
           text.slice(1);
}


// =========================
// Auto Refresh
// =========================

setInterval(() => {

    console.log(
        `Refreshing ${selectedDistrict}...`
    );

    fetchWeather(selectedDistrict);

}, 30000);


// =========================
// Initial Load
// =========================

fetchWeather(selectedDistrict);