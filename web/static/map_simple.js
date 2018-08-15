function initMap() {
  var map;
  var bounds = new google.maps.LatLngBounds();

  var markStr = document.getElementById('map').getAttribute('data-lat-lon');
  var newmarkers = markStr.split(',');
  var markers = [];

  markers.push(newmarkers[0] + ", " + newmarkers[1]);
  markers.push(parseFloat(newmarkers[2]));
  markers.push(parseFloat(newmarkers[3]));
  console.log(markers)

  var mapOptions = {
    mapTypeId: 'roadmap',
    center: position
  };

  // Display a map on the page
  map = new google.maps.Map(document.getElementById("map"), mapOptions);

  map.setTilt(45);

  var infoWindow = new google.maps.InfoWindow();

  var content = ['<div class="info_content">' +
    '<h3>London Eye</h3>' +
    '<p>The London Eye is a giant Ferris wheel situated on the banks of the River Thames. The entire structure is 135 metres (443 ft) tall and the wheel has a diameter of 120 metres (394 ft).</p>' + '</div>'];
    
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
