from flask import Flask, render_template, url_for, request, send_from_directory
from datetime import datetime
import whoosh
import whoosh.index as indexUSE
from whoosh.analysis import *
indexer = indexUSE.open_dir("../indexedData")
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.searching import *

app = Flask(__name__)

class City:
    def __init__(self, city, state, date, avgHigh, avgLow, uvIndex, totalSunHours, avgSunHours, totalSnow, avgSnow, totalRainfall, avgRainfall, avgHumidity, avgPressure, avgWindSpeed):
        self.date = date
        self.city = city
        self.state = state
        self.avgHigh = avgHigh
        self.avgLow = avgLow
        self.uvIndex = uvIndex
        self.totalSunHours = totalSunHours
        self.avgSunHours = avgSunHours
        self.totalSnow = totalSnow
        self.avgSnow = avgSnow
        self.totalRainfall = totalRainfall
        self.avgRainfall = avgRainfall
        self.avgHumidity = avgHumidity
        self.avgPressure = avgPressure
        self.avgWindSpeed = avgWindSpeed


@app.route('/', methods=['GET', 'POST'])
def home():
    print("At home page")
    return render_template("homePage.html")

# For static files that HTML requests. Like the CSS file.


@app.route('/static/<path:path>')
def send_file(path):
    print("in here {}".format(path))
    return send_from_directory('text/css', path)


@app.route('/results/', methods=['GET'])
def results():
    data = request.args
    print(data)
    query = data.get('searchterm').title()
    
    beginDate = data.get('beginDate')
    endDate = data.get('endDate')
    minTemp = data.get('minTemp')
    maxTemp = data.get('maxTemp')
    # SHANE ENTER YOUR WHOOSH INDEX HERE
    # FOR the begin dates and end dates, first check if = '', then use strftime(date, "%Y-%m")

    searchTerm = query
    splitSearch = searchTerm.split(',')
   

    if (len(splitSearch) > 1):
        splitSearch[0].strip()
        splitSearch[1].strip()
        searchTerm = "{} AND {}".format(splitSearch[0], splitSearch[1])
    if (beginDate == ''):
        beginDate = "2017-6"
    searchTerm += " [{} to ".format(beginDate)
   
    if (endDate == ''):
        endDate = "2018-6" 
    searchTerm += "{}] ".format(endDate)

    if (minTemp == ''):
        minTemp = "-80"
    
    if (maxTemp == ''):
        maxTemp = "140"

    print("searchterm: {}".format(searchTerm))
    with indexer.searcher() as searcher:
        queryTest = MultifieldParser(["City", "avgTemp", "avgLow", "avgHigh", "State", "Date"], schema=indexer.schema).parse(searchTerm)
        nr = NumericRange("avgTemp", int(minTemp), int(maxTemp));
        # np = query.Term("Index", 151);
        
        results = searcher.search(queryTest, filter=nr, limit=None)
        print("Length of results: " + str(len(results)))
        Cities = {}
        for line in results:
            print(line)

    print("You searched for: " + query)
    
    return render_template('results.html', query=query)


@app.route('/city/', methods=['GET', 'POST'])
def city():
    data = request.args

    cityName = data.get('city')
    stateName = data.get('state')

    # Get data about city from query
    city = []
    city.append(City("New York", "New York", "2017/7", 88.48, 77.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 3.94, 0.13, 64.42, 1014.68, 10.26))
    city.append(City("New York", "New York", "2017/8", 88.48, 77.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 3.94, 0.13, 64.42, 1014.68, 10.26))
    return render_template('city.html', city=city)


if (__name__ == '__main__'):
    app.run(debug=True)
