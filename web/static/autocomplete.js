searchBar = document.getElementById('searchbar');

function autocomplete(key) {
    var req = new XMLHttpRequest();
    var val = key;
    var a, b, i;
    var url = "/search?val=" + val;
    req.open("GET", url, false);
    // req.responseType = 'text';
    req.onload = function() {
        var res = req.response.split(',');
        console.log(res);
        return res;
        // searchBar.value = req.response;
    }
    req.send();
    
}
var currentFocus;
searchBar.addEventListener("input", function (e) {
    var arr = ['New York, New York','Los Angeles, California','Chicago, Illinois','Houston, Texas','Phoenix, Arizona','Philadelphia, Pennsylvania','San Antonio, Texas','San Diego, California','Dallas, Texas','San Jose, California','Austin, Texas','Jacksonville, Florida','San Francisco, California','Columbus, Ohio','Fort Worth, Texas','Indianapolis, Indiana','Charlotte, North Carolina','Seattle, Washington','Denver, Colorado','Washington, District of Columbia','Boston, Massachusetts','El Paso, Texas','Detroit, Michigan','Nashville, Tennessee','Memphis, Tennessee','Portland, Oregon','Oklahoma City, Oklahoma','Las Vegas, Nevada','Louisville, Kentucky','Baltimore, Maryland','Milwaukee, Wisconsin','Albuquerque, New Mexico','Tucson, Arizona','Fresno, California','Sacramento, California','Mesa, Arizona','Kansas City, Missouri','Atlanta, Georgia','Long Beach, California','Omaha, Nebraska','Raleigh, North Carolina','Colorado Springs, Colorado','Miami, Florida','Virginia Beach, Virginia','Oakland, California','Minneapolis, Minnesota','Tulsa, Oklahoma','Arlington, Texas','New Orleans, Louisiana','Wichita, Kansas','Cleveland, Ohio','Tampa, Florida','Bakersfield, California','Aurora, Colorado','Anaheim, California','Honolulu, Hawaii','Santa Ana, California','Riverside, California','Corpus Christi, Texas','Lexington, Kentucky','Stockton, California','St. Louis, Missouri','Saint Paul, Minnesota','Henderson, Nevada','Pittsburgh, Pennsylvania','Cincinnati, Ohio','Anchorage, Alaska','Greensboro, North Carolina','Plano, Texas','Newark, New Jersey','Lincoln, Nebraska','Orlando, Florida','Irvine, California','Toledo, Ohio','Jersey City, New Jersey','Chula Vista, California','Durham, North Carolina','Fort Wayne, Indiana','St. Petersburg, Florida','Laredo, Texas','Buffalo, New York','Madison, Wisconsin','Lubbock, Texas','Chandler, Arizona','Scottsdale, Arizona','Reno, Nevada','Glendale, Arizona','Norfolk, Virginia','Winston Salem, North Carolina','North Las Vegas, Nevada','Gilbert, Arizona','Chesapeake, Virginia','Irving, Texas','Hialeah, Florida','Garland, Texas','Fremont, California','Richmond, Virginia','Boise, Idaho','Baton Rouge, Louisiana','Des Moines, Iowa','Spokane, Washington','San Bernardino, California','Modesto, California','Tacoma, Washington','Fontana, California','Santa Clarita, California','Birmingham, Alabama','Oxnard, California','Fayetteville, North Carolina','Rochester, New York','Moreno Valley, California','Glendale, California','Yonkers, New York','Huntington Beach, California','Aurora, Illinois','Salt Lake City, Utah','Amarillo, Texas','Montgomery, Alabama','Grand Rapids, Michigan','Little Rock, Arkansas','Akron, Ohio','Augusta, Georgia','Huntsville, Alabama','Columbus, Georgia','Grand Prairie, Texas','Shreveport, Louisiana','Overland Park, Kansas','Tallahassee, Florida','Mobile, Alabama','Port St. Lucie, Florida','Knoxville, Tennessee','Worcester, Massachusetts','Tempe, Arizona','Cape Coral, Florida','Brownsville, Texas','McKinney, Texas','Providence, Rhode Island','Fort Lauderdale, Florida','Newport News, Virginia','Chattanooga, Tennessee','Rancho Cucamonga, California','Frisco, Texas','Sioux Falls, South Dakota','Oceanside, California','Ontario, California','Vancouver, Washington','Santa Rosa, California','Garden Grove, California','Elk Grove, California','Pembroke Pines, Florida','Salem, Oregon','Eugene, Oregon','Peoria, Arizona','Corona, California','Springfield, Missouri','Jackson, Mississippi','Cary, North Carolina','Fort Collins, Colorado','Hayward, California','Lancaster, California','Alexandria, Virginia','Salinas, California','Palmdale, California','Lakewood, Colorado','Springfield, Massachusetts','Sunnyvale, California','Hollywood, Florida','Pasadena, Texas','Clarksville, Tennessee','Pomona, California','Kansas City, Kansas','Macon, Georgia','Escondido, California','Paterson, New Jersey','Joliet, Illinois','Naperville, Illinois','Rockford, Illinois','Torrance, California','Bridgeport, Connecticut','Savannah, Georgia','Killeen, Texas','Bellevue, Washington','Mesquite, Texas','Syracuse, New York','McAllen, Texas','Pasadena, California','Orange, California','Fullerton, California','Dayton, Ohio','Miramar, Florida','Olathe, Kansas','Thornton, Colorado','Waco, Texas','Murfreesboro, Tennessee','Denton, Texas','West Valley City, Utah','Midland, Texas','Carrollton, Texas','Roseville, California','Warren, Michigan','Charleston, South Carolina','Hampton, Virginia','Surprise, Arizona','Columbia, South Carolina','Coral Springs, Florida','Visalia, California','Sterling Heights, Michigan','Gainesville, Florida','Cedar Rapids, Iowa','New Haven, Connecticut','Stamford, Connecticut','Elizabeth, New Jersey','Concord, California','Thousand Oaks, California','Kent, Washington','Santa Clara, California','Simi Valley, California','Lafayette, Louisiana','Topeka, Kansas','Athens, Georgia','Round Rock, Texas','Hartford, Connecticut','Norman, Oklahoma','Victorville, California','Fargo, North Dakota','Berkeley, California','Vallejo, California','Abilene, Texas','Columbia, Missouri','Ann Arbor, Michigan','Allentown, Pennsylvania','Pearland, Texas','Beaumont, Texas','Wilmington, North Carolina','Evansville, Indiana','Arvada, Colorado','Provo, Utah','Independence, Missouri','Lansing, Michigan','Odessa, Texas','Richardson, Texas','Fairfield, California','El Monte, California','Rochester, Minnesota','Clearwater, Florida','Carlsbad, California','Springfield, Illinois','Temecula, California','West Jordan, Utah','Costa Mesa, California','Miami Gardens, Florida','Cambridge, Massachusetts','College Station, Texas','Murrieta, California','Downey, California','Peoria, Illinois','Westminster, Colorado','Elgin, Illinois','Antioch, California','Palm Bay, Florida','High Point, North Carolina','Lowell, Massachusetts','Manchester, New Hampshire','Pueblo, Colorado','Gresham, Oregon','North Charleston, South Carolina','Ventura, California','Inglewood, California','Pompano Beach, Florida','Centennial, Colorado','West Palm Beach, Florida','Everett, Washington','Richmond, California','Clovis, California','Billings, Montana','Waterbury, Connecticut','Broken Arrow, Oklahoma','Lakeland, Florida','West Covina, California','Boulder, Colorado','Daly City, California','Santa Maria, California','Hillsboro, Oregon','Sandy Springs, Georgia','Norwalk, California','Jurupa Valley, California','Lewisville, Texas','Greeley, Colorado','Davie, Florida','Green Bay, Wisconsin','Tyler, Texas','League City, Texas','Burbank, California','San Mateo, California','Wichita Falls, Texas','El Cajon, California','Rialto, California','Lakewood, New Jersey','Edison, New Jersey','Davenport, Iowa','South Bend, Indiana','Woodbridge, New Jersey','Las Cruces, New Mexico','Vista, California','Renton, Washington','Sparks, Nevada','Clinton, Michigan','Allen, Texas','Tuscaloosa, Alabama','San Angelo, Texas','Vacaville, California','Corvallis, Oregon','Beaverton, Oregon','Medford, Oregon','Bend, Oregon','Newport, Oregon'];
    var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      b = document.createElement("DIV");
      b.innerHTML = "<strong>" + val + "</strong>";
      b.innerHTML += "<input type='hidden' value='" + val + "'>";
      b.addEventListener("click", function(e) {
        /*insert the value for the autocomplete text field:*/
        searchBar.value = this.getElementsByTagName("input")[0].value;
        closeAllLists();
      });
      a.appendChild(b);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        var reg = new RegExp(val, 'i');
        var match = arr[i].match(reg);
        if (match != null) {
          var idx = arr[i].toUpperCase().indexOf(val.toUpperCase());
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "";
          if (idx != 0) {
            b.innerHTML += arr[i].substr(0, idx);
          }
          b.innerHTML += "<strong>" + match[0] + "</strong>";
          b.innerHTML += arr[i].substr(idx + val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              searchBar.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
});
searchBar.addEventListener("keydown", function(e) {
    var sbmt = document.getElementById('submit-btn');
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      /*If the arrow DOWN key is pressed,
      increase the currentFocus variable:*/
      currentFocus++;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 38) { //up
      /*If the arrow UP key is pressed,
      decrease the currentFocus variable:*/
      currentFocus--;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 13 || e.keyCode == 39) {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (x) x[currentFocus].click();
        currentFocus = -1
      }
      else {
        sbmt.click();
      }
    }
});
function addActive(x) {
  /*a function to classify an item as "active":*/
  if (!x) return false;
  /*start by removing the "active" class on all items:*/
  removeActive(x);
  if (currentFocus >= x.length) currentFocus = 0;
  if (currentFocus < 0) currentFocus = (x.length - 1);
  /*add class "autocomplete-active":*/
  x[currentFocus].classList.add("autocomplete-active");
}
function removeActive(x) {
  /*a function to remove the "active" class from all autocomplete items:*/
  for (var i = 0; i < x.length; i++) {
    x[i].classList.remove("autocomplete-active");
  }
}
function closeAllLists(elmnt) {
  /*close all autocomplete lists in the document,
  except the one passed as an argument:*/
  var x = document.getElementsByClassName("autocomplete-items");
  for (var i = 0; i < x.length; i++) {
    if (elmnt != x[i] && elmnt != searchBar) {
    x[i].parentNode.removeChild(x[i]);
  }
}
}
/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
  closeAllLists(e.target);
});

