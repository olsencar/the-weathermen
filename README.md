# the-weathermen
Final Project - CS 340

Using API from https://developer.worldweatheronline.com/api/historical-weather-api.aspx

List of popular cities: https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population

Folders

    1. indexedData: This is where the indexed data is stored.

    2. weather_data: This is where all of our csv weather data is stored.

    3. web: This is where all of our website code is stored.

To run the Whoosh index:

    1. Delete the indexedData folder if it exists

    2. Run the whooshIndexing.py file using 'python whooshIndexing.py'

    3. Let it run

To run the server:

    1. Change to the web directory

    2. Run the server.py file using 'python server.py'

    3. The server should run on localhost:5000