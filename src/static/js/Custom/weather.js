const weatherBlock = document.querySelector(".weather-block");
const weatherBlockBtn = document.querySelector(".weather-btn");
let isWeatherClicked = true;
const dynamicWeather = document.getElementById("dynamic-weather");
let currentWeather = document.querySelector(".current-weather")
const simulator = document.querySelector(".simulator");


//Display / hide weather
weatherBlockBtn.addEventListener('click', (e) => {
    e.preventDefault();
    isWeatherClicked = !isWeatherClicked;
    weatherBlock.style.display = isWeatherClicked ? "block" : "none";
    adjustAladinContainer();
});

if (currentWeather) {
    dynamicWeather.style.display = "block";
}

// // Adjust Aladin container based on weather block visibility
// function adjustAladinContainer() {
//     if (isWeatherClicked) {
//         //simulator.style.width = "calc(100% - 300px)"; // Adjust the width based on your weather block width
//         //simulator.style.marginLeft = "300px"; // Adjust margin to account for the width of the weather block
//     } else {
//         simulator.style.width = "100%";
//         simulator.style.margin = "0 auto";
//     }
// }
//
// // Initial adjustment
// adjustAladinContainer();
