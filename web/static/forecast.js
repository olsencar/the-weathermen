API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/weather.ashx";
API_KEY = "7826c9f4779b4375b89185008181207";
var script = document.createElement(script);
script.src = "https://code.jquery.com/jquery-3.3.1.min.js";
script.integrity = "sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=";
script.crossorigin = "anonymous"

document.getElementsByTagName('head')[0].appendChild(script);

var resultContainer = $("#weather-forecast");
var output = '';
$(document).ready(function () {
    
    var query = $("#city-state").text().trim().replace(/\s/g,'+');
    console.log(query);
    var url = API_ENDPOINT + '?q=' + query + '&format=JSON' + '&num_of_days=6' + '&tp=24' + '&mca=no' + '&key=' + API_KEY;
    $.ajax({
        type: 'GET',
        url: url,
        async: false,
        contentType: "application/json",
        jsonpCallback: "LocalWeatherCallback",
        dataType: 'jsonp',
        success: function (json) {
            console.log('success');
        },
        error: function (e) {
            console.log(e.message);
        }
    });    
});
function LocalWeatherCallback(localWeather) {
    var weather = localWeather.data.weather;
    
    for (var i = 0; i < weather.length; i++) {
        output += "<div class='col-md-2 panel panel-default text-left'>" + "<div class='attr-container panel-heading text-center'> <h4>" + weather[i].date + "</h4> </div>" + "<img src=" + weather[i].hourly[0].weatherIconUrl[0].value + ">" + "<div class='attr-container panel-body'> <strong> Low: </strong>" + weather[i].mintempF + "&deg;F </div>" + "<div class='attr-container panel-body'> <strong> High: </strong>" + weather[i].maxtempF + "&deg;F </div>" + "<div class='attr-container panel-body'> <strong> UV Index: </strong>" + weather[i].uvIndex + "</div>" + "<div class='attr-container panel-body'> <strong> Wind: </strong>" + weather[i].hourly[0].windspeedMiles + " MPH " + weather[i].hourly[0].winddirDegree + "&deg; " + weather[i].hourly[0].winddir16Point + "</div>" + "<div class='attr-container panel-body'>" + weather[i].hourly[0].weatherDesc[0].value + "</div>"
        output += "</div>"
    }
    
    // output = "<br/> Cloud Cover: " + localWeather.data.current_condition[0].cloudcover;
    // output += "<br/> Humidity: " + localWeather.data.current_condition[0].humidity;
    // output += "<br/> Temp C: " + localWeather.data.current_condition[0].temp_C;
    // output += "<br/> Visibility: " + localWeather.data.current_condition[0].weatherDesc[0].value;
    // output += "<br/> Observation Time: " + localWeather.data.current_condition[0].observation_time;
    // output += "<br/> Pressue: " + localWeather.data.current_condition[0].pressure;

    resultContainer.empty();
    resultContainer.html(output);
}



// function LocalWeatherCallback(localWeather) {
//     var weatherdata = localWeather.data.weather;

//     for (var i = 0; i < weatherdata.length; i++) {
//         console.log(weatherdata[i].date);
//     }
//     output = "<br/> Cloud Cover: " + localWeather.data.current_condition[0].cloudcover;
//     output += "<br/> Humidity: " + localWeather.data.current_condition[0].humidity;
//     output += "<br/> Temp C: " + localWeather.data.current_condition[0].temp_C;
//     output += "<br/> Visibility: " + localWeather.data.current_condition[0].weatherDesc[0].value;
//     output += "<br/> Observation Time: " + localWeather.data.current_condition[0].observation_time;
//     output += "<br/> Pressue: " + localWeather.data.current_condition[0].pressure;

//     resultContainer.empty();
//     resultContainer.html(output);

// }