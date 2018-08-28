function changeInfoWindow() {
    var infoWindow = document.getElementsByClassName('gm-style-iw');
    var parent = infoWindow.parentElement;

    parent.style.wordWrap = "normal";
    parent.style.padding = "2px";
    parent.style.width = "auto";
}

function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        if (value === undefined) {
            value = "";
        }
        vars[key] = value;
    });
    return vars;
}

function initialize() {
    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'
    };

    // Display a map on the page
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
    map.setTilt(45);

    var markStr = document.getElementById('map').getAttribute('data-lat-lon');
    //var markHigh = document.getElementById('map').getAttribute('high');
    //var markLow = document.getElementById('map').getAttribute('low');
    //console.log(markHigh)
    //console.log(markLow)
    var newmarkers = markStr.split(',');
    var markers = [];

    for (var i = 0; i < newmarkers.length; i++) {
        var temp = [];
        if (i % 6 == 0) {
            temp.push(newmarkers[i - 6] + ", " + newmarkers[i - 5]); // City, State
            temp.push(parseFloat(newmarkers[i - 4])); // Lat
            temp.push(parseFloat(newmarkers[i - 3])); // Long
            temp.push(parseFloat(newmarkers[i - 2])); // Low
            temp.push(parseFloat(newmarkers[i - 1])); // High
            markers.push(temp);
        }
    }
    markers.shift()
    // Multiple Markers

    // Display multiple markers on a map
    var infoWindow = new google.maps.InfoWindow();

    var params = getUrlVars();
    // Loop through our array of markers & place each one on the map
    for( i = 0; i < markers.length; i++ ) {
        // Info Window Content
        var cityState = markers[i][0].split(',');
        for (var j = 0; j < cityState.length; j++) {
            cityState[j].trim();
        }
        var content = [
          '<div class="info_content">' +
          '<h2><a href="/city?searchterm=' + String(markers[i][0]) + '&city=' + cityState[0] + '&state=' + cityState[1] + '&beginDate=' + params['beginDate'] + '&endDate=' + params['endDate'] + '&minTemp=' + params['minTemp'] + '&maxTemp=' + params['maxTemp'] + '">' + String(markers[i][0]) + '</a></h2>' +
          '<h4>' + 'Min Temp: ' +  String(markers[i][3]) + '</h4>' +
          '<h4>' + 'Max Temp: ' +  String(markers[i][4]) + '</h4>' +
          '</div>'
        ];

        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            title: markers[i][0]
        });

        // Allow each marker to have an info window
        google.maps.event.addListener(marker, 'click', (function(marker, content, infoWindow) {
            return function() {
                var c = String(content);
                infoWindow.setContent(c);
                // infoWindow.setContent(infoWindow.getContent());
                infoWindow.open(map,marker);
            }
        })(marker, content, infoWindow));

    }
    var position = new google.maps.LatLng(39.709052666183865, -99.63684006313935);
    map.setCenter(position);
    map.setZoom(map.getZoom());
    // google.maps.event.addListenerOnce(map, 'bounds_changed', function(event) {
    //     this.setZoom(map.getZoom());

    //     if (this.getZoom() > 15) {
    //       this.setZoom(15);
    //     }
    // });
    map.fitBounds(bounds);


    // // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
    // var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
    //     this.setZoom(14);
    //     google.maps.event.removeListener(boundsListener);
    // });
    google.maps.event.addDomListener(window, 'load', initialize)

    changeInfoWindow();
}
