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
    def __init__(self, city, state, date, avgHigh, avgLow, uvIndex, totalSunHours, avgSunHours, totalSnow, avgSnow, totalRainfall, avgRainfall, avgHumidity, avgPressure, avgWindSpeed, avgTemp):
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
        self.avgTemp = avgTemp


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
        
        r = searcher.search(queryTest, filter=nr, limit=None)
        print("Length of results: " + str(len(r)))
        arr = []
        Cities = {}
        for line in r:
            if line['City'] in Cities:
                pass;
            else:
                Cities[line['City']] = line['State'];
            arr.append(City(line['City'], line['State'], datetime.strftime(line['Date'], "%Y-%m"), line['avgHigh'], line['avgLow'],line['avgUV'], line['totalSun'], line['avgSun'],line['totalSnow'], line['avgSnow'], line['totalRainfall'], line['avgRainfall'], line['avgHumidity'], line['pressure'], line['windSpeed'], line['avgTemp']))
        for key in Cities:
            print("City: " + key + " State: " + Cities[key]);

    fp = open("../locations.csv", "r");
    head = next(fp);
    Lat = [];
    Long = [];
    for line in fp:
        row  = line.split(",");
        for i in Cities:
            if (i == row[1]):
                latStr = row[3][0] + row[3][1] + ".";
                dec = float(row[3][4] + row[3][5])/60 + float(row[3][7] + row[3][8])/3600;
                latStr = latStr + str(dec);
                latStr = latStr[0:2] + latStr[4:]
                Lat.append(latStr);
                if (int(row[4][2]) >= 0 and int(row[4][2]) <=9):
                    longStr = row[4][0] + row[4][1] + row[4][2] + ".";
                    dec = float(row[4][5] + row[4][6])/60 + float(row[4][8] + row[4][9])/3600;
                    longStr = longStr + str(dec);
                    longStr = longStr[0:2] + longStr[4:]
                    Long.append(longStr);
                else:
                    longStr = row[4][0] + row[4][1] + ".";
                    dec = float(row[4][4] + row[4][5])/60 + float(row[4][7] + row[4][8])/3600;
                    longStr = longStr + str(dec);
                    longStr = longStr[0:2] + longStr[4:]
                    Long.append(longStr);
    print(Lat);
    print(Long);


    print("You searched for: " + query)
    if (len(Cities) > 1):
        return render_template('results.html', query=query, results=Cities, searchterm=searchTerm)    
    
    return render_template('city.html', query=query, results=arr, searchterm=searchTerm)


@app.route('/city', methods=['GET', 'POST'])
def city():
    data = request.args

    # cityName = data.get('city')
    # stateName = data.get('state')
    searchterm = data.get('searchterm')
    # print(searchterm)
    # Get data about city from query
    city = []
    # city.append(City("New York", "New York", "2017/7", 88.48, 77.0,
    #                  0.0, 0.0, 0.0, 0.0, 0.0, 3.94, 0.13, 64.42, 1014.68, 10.26))
    # city.append(City("New York", "New York", "2017/8", 88.48, 77.0,
    #                  0.0, 0.0, 0.0, 0.0, 0.0, 3.94, 0.13, 64.42, 1014.68, 10.26))
    return render_template('city.html', city=searchterm)


if (__name__ == '__main__'):
    app.run(debug=True)
