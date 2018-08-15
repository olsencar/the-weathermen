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
    var newmarkers = markStr.split(',');
    var markers = [];
    
    if (newmarkers.length === 4) {
        var temp = [];
        temp.push(newmarkers[0] + ", " + newmarkers[1]);
        temp.push(parseFloat(newmarkers[2]));
        temp.push(parseFloat(newmarkers[3]));
        markers.push(temp);
        console.log(temp)
        
    }
    else {
        for (var i = 0; i < newmarkers.length; i++) {
            
            var temp = [];
            if (i % 4 == 0) {
                temp.push(newmarkers[i - 4] + ", " + newmarkers[i - 3]);
                temp.push(parseFloat(newmarkers[i - 2]));
                temp.push(parseFloat(newmarkers[i - 1]));
                markers.push(temp);
                console.log(temp)
            } 

        }
    }
    markers.shift()
    // Multiple Markers

    // Info Window Content
    var content = ['<div class="info_content">' +
        '<h3>London Eye</h3>' +
        '<p>The London Eye is a giant Ferris wheel situated on the banks of the River Thames. The entire structure is 135 metres (443 ft) tall and the wheel has a diameter of 120 metres (394 ft).</p>' +        '</div>'];

    // Display multiple markers on a map
    var infoWindow = new google.maps.InfoWindow();

    // Loop through our array of markers & place each one on the map
    for( i = 0; i < markers.length; i++ ) {
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

}

