/*
    This file is intended for pages that include the single-marker Google Map.
    Used on the client side to render a map with one marker.
 */


function initMap() {
  var map;
  var bounds = new google.maps.LatLngBounds();

  var markStr = document.getElementById('map').getAttribute('data-lat-lon');
  var markHigh = document.getElementById('map').getAttribute('high');
  var markLow = document.getElementById('map').getAttribute('low');
  console.log(markHigh)
  console.log(markLow)
  var newmarkers = markStr.split(',');
  var markers = [];

  markers.push(newmarkers[0] + ", " + newmarkers[1]);
  markers.push(parseFloat(newmarkers[2]));
  markers.push(parseFloat(newmarkers[3]));
  markers.push(parseFloat(newmarkers[4]));
  markers.push(parseFloat(newmarkers[5]));
  console.log(markers)

  var mapOptions = {
    mapTypeId: 'roadmap',
    center: position
  };

  // Display a map on the page
  map = new google.maps.Map(document.getElementById("map"), mapOptions);

  map.setTilt(45);

  var infoWindow = new google.maps.InfoWindow();

  var content = [
    '<center><div class="info_content">' +
    '<h2>' + String(markers[0]) + '</h2>' +
    '<h4>' + 'Low: ' +  String(markers[3]) + '</h4>' +
    '<h4>' + 'High: ' +  String(markers[4]) + '</h4>' +
    '</div></center>'
  ];

  var position = new google.maps.LatLng(markers[1], markers[2]);
  bounds.extend(position);
  marker = new google.maps.Marker({
    position: position,
    map: map,
    title: markers[0]
  });

  // Allow each marker to have an info window
  google.maps.event.addListener(marker, 'click', (function (marker, content, infoWindow) {
    return function () {
      var c = String(content);
      infoWindow.setContent(c);
      // infoWindow.setContent(infoWindow.getContent());
      infoWindow.open(map, marker);
    }
  })(marker, content, infoWindow));

  map.setZoom(map.getZoom());
  google.maps.event.addListenerOnce(map, 'bounds_changed', function(event) {
      this.setZoom(6);
  });
  map.fitBounds(bounds);

}
