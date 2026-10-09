/* Atmos Weather Dashboard
   Configure API_BASE if your FastAPI server runs on another host/port.
*/
const API_BASE = "http://127.0.0.1:8000";
const DISTRICTS = ["Meerut", "Ghaziabad", "Noida", "Lucknow", "Agra", "Kanpur", "Varanasi"];

const $ = (id) => document.getElementById(id);
let currentDistrict = "Meerut";
let currentWeather = null;

document.addEventListener("DOMContentLoaded", () => {
  $("todayDate").textContent = new Intl.DateTimeFormat("en-IN", {
    weekday: "long", day: "numeric", month: "short", year: "numeric"
  }).format(new Date());
  $("year").textContent = new Date().getFullYear();

  $("districtSelect").addEventListener("change", (event) => {
    currentDistrict = event.target.value;
    $("selectedDistrictLabel").textContent = `${currentDistrict}, India`;
  });
  $("loadBtn").addEventListener("click", () => loadWeather(currentDistrict));
  $("refreshBtn").addEventListener("click", () => loadWeather(currentDistrict));
  $("historyRefresh").addEventListener("click", () => loadHistory(currentDistrict));
  $("dismissError").addEventListener("click", hideError);
  $("menuToggle").addEventListener("click", () => $("sidebar").classList.toggle("open"));

  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => switchView(button.dataset.view, button));
  });

  loadWeather(currentDistrict);
});

function switchView(view, button) {
  document.querySelectorAll(".nav-item").forEach((item) => item.classList.toggle("active", item === button));
  ["overview", "conditions", "history"].forEach((name) => {
    $(`${name}View`).classList.toggle("hidden", name !== view);
  });
  $("pageTitle").textContent = ({ overview: "Overview", conditions: "Conditions", history: "Recent records" })[view];
  $("sidebar").classList.remove("open");
  if (view === "conditions" && currentWeather) renderDetails(currentWeather);
  if (view === "history") loadHistory(currentDistrict);
}

async function loadWeather(district) {
  setLoading(true);
  hideError();
  try {
    const response = await fetch(`${API_BASE}/api/weather/${encodeURIComponent(district.toLowerCase())}`);
    if (!response.ok) {
      const body = await safeJson(response);
      throw new Error(body.detail || `Weather API returned ${response.status}.`);
    }
    const data = await response.json();
    const record = normalizeWeather(data);
    if (record.temperature === null && record.humidity === null) {
      throw new Error("The API responded, but no usable weather fields were found.");
    }
    currentWeather = record;
    renderWeather(record);
    setConnection(true, "Connected to API");
  } catch (error) {
    setConnection(false, "API unavailable");
    showError(`${error.message} Make sure FastAPI is running and its response fields match the database.`);
  } finally {
    setLoading(false);
  }
}

async function safeJson(response) {
  try { return await response.json(); } catch { return {}; }
}

/* Supports API responses containing a weather object or a direct record. */
function normalizeWeather(payload) {
  const data = payload?.weather ?? payload?.data ?? payload;
  return {
    district: first(data, ["district", "location", "city"]) || currentDistrict,
    time: first(data, ["time", "timestamp", "observation_time", "updated_at"]),
    temperature: numberOrNull(first(data, ["temperature_2m", "temperature", "temp"])),
    feelsLike: numberOrNull(first(data, ["apparent_temperature", "feels_like"])),
    humidity: numberOrNull(first(data, ["relative_humidity_2m", "humidity"])),
    wind: numberOrNull(first(data, ["wind_speed_10m", "wind_speed", "windspeed"])),
    pressure: numberOrNull(first(data, ["pressure_msl", "pressure"])),
    rain: numberOrNull(first(data, ["rain", "rainfall"])),
    precipitation: numberOrNull(first(data, ["precipitation"])),
    showers: numberOrNull(first(data, ["showers"])),
    snowfall: numberOrNull(first(data, ["snowfall"])),
    cloud: numberOrNull(first(data, ["cloud_cover", "cloudcover"])),
    direction: numberOrNull(first(data, ["wind_direction_10m", "wind_direction", "winddirection"])),
    gusts: numberOrNull(first(data, ["wind_gusts_10m", "wind_gusts", "windgusts"])),
    latitude: numberOrNull(first(data, ["latitude"])),
    longitude: numberOrNull(first(data, ["longitude"])),
    timezone: first(data, ["timezone"]) || "—"
  };
}

function first(obj, keys) {
  for (const key of keys) if (obj && obj[key] !== undefined && obj[key] !== null) return obj[key];
  return null;
}
function numberOrNull(value) {
  if (value === null || value === undefined || value === "") return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}
function fmt(value, digits = 1) { return value === null ? "—" : Number(value).toFixed(digits).replace(/\.0$/, ""); }
function renderWeather(w) {
  $("selectedDistrictLabel").textContent = `${w.district}, India`;
  $("heroDistrict").textContent = w.district;
  $("temperature").textContent = fmt(w.temperature);
  $("conditionText").textContent = getCondition(w);
  $("feelsLike").textContent = `Feels like ${fmt(w.feelsLike)}°C`;
  $("humidity").textContent = fmt(w.humidity, 0);
  $("windSpeed").textContent = fmt(w.wind);
  $("pressure").textContent = fmt(w.pressure);
  $("rainfall").textContent = fmt(w.rain);
  $("humidityBar").style.width = `${Math.max(0, Math.min(100, w.humidity ?? 0))}%`;
  $("windDirection").textContent = w.direction === null ? "—" : `${fmt(w.direction, 0)}° ${directionLabel(w.direction)}`;
  $("windGusts").textContent = fmt(w.gusts);
  $("observationTime").textContent = formatDate(w.time);
  $("lastUpdated").textContent = formatTime(w.time) || new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  renderAlert(w);
  $("windNote").textContent = w.wind === null ? "Wind readings are not available." :
    w.wind >= 35 ? "Strong winds recorded. Secure loose outdoor objects." :
    w.wind >= 20 ? "Moderate to strong breeze in the latest reading." :
    "Wind speeds are relatively light in the latest reading.";
  renderDetails(w);
}
function getCondition(w) {
  if ((w.rain ?? 0) > 0 || (w.precipitation ?? 0) > 0 || (w.showers ?? 0) > 0) return "Rain observed";
  if ((w.snowfall ?? 0) > 0) return "Snowfall observed";
  if (w.cloud !== null && w.cloud >= 75) return "Cloudy";
  if (w.cloud !== null && w.cloud >= 35) return "Partly cloudy";
  if (w.temperature !== null && w.cloud !== null) return "Clear conditions";
  return "Current conditions";
}
function renderAlert(w) {
  const rain = w.rain ?? 0;
  const precip = w.precipitation ?? 0;
  const showers = w.showers ?? 0;
  let title = "No rainfall detected";
  let message = "No rainfall is recorded in the latest observation.";
  let tone = "good";
  if (rain >= 7.5 || precip >= 7.5 || showers >= 7.5) {
    title = "Heavy rainfall observed";
    message = "Significant rainfall is recorded. Take care in low-lying or waterlogged areas.";
    tone = "danger";
  } else if (rain > 0 || precip > 0 || showers > 0) {
    title = "Rain detected";
    message = "Rainfall is present in the latest observation. Conditions may change.";
    tone = "warning";
  }
  $("alertTitle").textContent = title;
  $("alertMessage").textContent = message;
  $("alertIndicator").className = `alert-indicator ${tone}`;
  $("alertSymbol").className = `alert-symbol ${tone}`;
  $("alertSymbol").innerHTML = tone === "danger" ? '<i class="bi bi-exclamation-triangle"></i>' :
    tone === "warning" ? '<i class="bi bi-cloud-rain"></i>' : '<i class="bi bi-cloud-check"></i>';
}
function renderDetails(w) {
  const details = [
    ["Temperature", w.temperature, "°C"], ["Feels like", w.feelsLike, "°C"],
    ["Relative humidity", w.humidity, "%"], ["Precipitation", w.precipitation, "mm"],
    ["Rain", w.rain, "mm"], ["Showers", w.showers, "mm"],
    ["Snowfall", w.snowfall, "cm"], ["Cloud cover", w.cloud, "%"],
    ["Sea-level pressure", w.pressure, "hPa"], ["Wind speed", w.wind, "km/h"],
    ["Wind direction", w.direction, "°"], ["Wind gusts", w.gusts, "km/h"],
    ["Latitude", w.latitude, ""], ["Longitude", w.longitude, ""], ["Timezone", w.timezone, ""]
  ];
  $("detailsGrid").innerHTML = details.map(([label, value, unit]) =>
    `<article class="detail-card"><span>${escapeHtml(label)}</span><strong>${value === null || value === "—" ? "—" : escapeHtml(fmtIfNumber(value))} <small>${escapeHtml(unit)}</small></strong></article>`
  ).join("");
}
function fmtIfNumber(value) { return typeof value === "number" ? fmt(value) : String(value); }
function directionLabel(degrees) {
  return ["N","NE","E","SE","S","SW","W","NW"][Math.round(degrees / 45) % 8];
}
function formatDate(value) {
  if (!value) return "—";
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? String(value) : d.toLocaleString([], { day:"2-digit", month:"short", hour:"2-digit", minute:"2-digit" });
}
function formatTime(value) {
  if (!value) return "";
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? String(value) : d.toLocaleTimeString([], { hour:"2-digit", minute:"2-digit" });
}
async function loadHistory(district) {
  const body = $("historyBody");
  body.innerHTML = '<tr><td colspan="6" class="table-empty">Loading recent records…</td></tr>';
  try {
    const response = await fetch(`${API_BASE}/api/weather/${encodeURIComponent(district.toLowerCase())}/history?limit=20`);
    if (!response.ok) throw new Error("History endpoint is not available.");
    const payload = await response.json();
    const rows = Array.isArray(payload) ? payload : (payload.records || payload.data || []);
    if (!rows.length) {
      body.innerHTML = '<tr><td colspan="6" class="table-empty">No recent records were returned.</td></tr>';
      return;
    }
    body.innerHTML = rows.map((row) => {
      const w = normalizeWeather(row);
      return `<tr><td>${escapeHtml(formatDate(w.time))}</td><td>${escapeHtml(fmt(w.temperature))} °C</td><td>${escapeHtml(fmt(w.humidity, 0))}%</td><td>${escapeHtml(fmt(w.wind))} km/h</td><td>${escapeHtml(fmt(w.rain))} mm</td><td>${escapeHtml(fmt(w.pressure))} hPa</td></tr>`;
    }).join("");
  } catch (error) {
    body.innerHTML = `<tr><td colspan="6" class="table-empty">${escapeHtml(error.message)} Use your existing latest-weather endpoint if history is not implemented.</td></tr>`;
  }
}
function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
  })[ch]);
}
function setConnection(connected, label) {
  $("connectionText").textContent = label;
  $("connectionDot").style.background = connected ? "#29c58c" : "#e35d6a";
  $("connectionDot").style.boxShadow = connected ? "0 0 0 4px #29c58c1b" : "0 0 0 4px #e35d6a1b";
}
function setLoading(loading) {
  $("loadBtn").disabled = loading;
  $("loadBtn").innerHTML = loading ? '<i class="bi bi-arrow-repeat"></i> Loading…' : '<i class="bi bi-search"></i> View weather';
  $("refreshBtn").classList.toggle("is-loading", loading);
}
function showError(message) {
  $("errorText").textContent = message;
  $("errorBanner").classList.remove("hidden");
}
function hideError() { $("errorBanner").classList.add("hidden"); }
