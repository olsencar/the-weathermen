from flask import Flask, render_template, url_for, request, send_from_directory
from datetime import datetime
import json
import whoosh
import whoosh.index as indexUSE
from whoosh.analysis import *
indexer = indexUSE.open_dir("../indexedData")
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.searching import *

app = Flask(__name__, static_folder="static")

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

def querySearch(searchTerm, beginDate, endDate, minTemp, maxTemp):
    splitSearch = searchTerm.split(',')
    
    if (len(splitSearch) > 1):
        splitSearch[0].strip()
        splitSearch[1].strip()
        
        searchTerm = "'{}' AND '{}')".format(splitSearch[0], splitSearch[1])

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
        arr = []
        Cities = {}
        for line in results:
            if line['City'] in Cities:
                pass;
            else:
                Cities[line['City']] = line['State'];
            arr.append(City(line['City'], line['State'], datetime.strftime(line['Date'], "%Y-%m"), line['avgHigh'], line['avgLow'],line['avgUV'], line['totalSun'], line['avgSun'],line['totalSnow'], line['avgSnow'], line['totalRainfall'], line['avgRainfall'], line['avgHumidity'], line['pressure'], line['windSpeed'], line['avgTemp']))
        for key in Cities:
            print("City: " + key + " State: " + Cities[key]);
    return results, Cities, arr

@app.route('/results', methods=['GET', 'POST'])
def results():
    data = request.args
    query = data.get('searchterm')
    cityName = data.get('city')
    stateName = data.get('state')
    minTemp = data.get('minTemp')
    maxTemp = data.get('maxTemp')
    beginDate = data.get('beginDate')
    endDate = data.get('endDate')

    searchTerm = query
    latnlon = ""
    results, Cities, arr = querySearch(searchTerm, beginDate, endDate, minTemp, maxTemp)
    fp = open("../locations.csv", "r");
    for line in fp:
        splitL = line.split(',')
        temp = [splitL[1],splitL[2], splitL[3], splitL[4].strip('\n')]
        for i in Cities:
            if (i == splitL[1]):
                print("{} = {}".format(i, splitL[1]))
                print(temp)
                latnlon += "{},{},{},{},".format(temp[0], temp[1], temp[2], temp[3])
                break;
    latnlon = latnlon[:-1] 
    
    fp.close()
    print("You searched for: " + query)
    if (len(Cities) > 1):
        return render_template('results.html', latnlon=latnlon, query=query, results=Cities, result2=arr, searchterm=searchTerm, minTemp=minTemp, maxTemp=maxTemp, beginDate=beginDate, endDate=endDate) 
    elif (len(Cities) == 0):
        return render_template('error.html')  
    else: 
        return render_template('city.html', results=arr)


@app.route('/city', methods=['GET', 'POST'])
def city():
    data = request.args

    cityName = data.get('city')
    stateName = data.get('state')
    minTemp = data.get('minTemp')
    maxTemp = data.get('maxTemp')
    beginDate = data.get('beginDate')
    endDate = data.get('endDate')

    searchTerm = data.get('searchterm')

    Cities = {}
    arr = []
    newArr = []
    results, Cities, arr = querySearch(searchTerm, beginDate, endDate, minTemp, maxTemp)
    
    if (len(Cities) > 1):
        for i in arr:
            if (i.city == cityName):
                newArr.append(i)
    
    print(searchTerm)
    # Get data about city from query
    
    # city.append(City("New York", "New York", "2017/7", 88.48, 77.0,
    #                  0.0, 0.0, 0.0, 0.0, 0.0, 3.94, 0.13, 64.42, 1014.68, 10.26))
    # city.append(City("New York", "New York", "2017/8", 88.48, 77.0,
    #                  0.0, 0.0, 0.0, 0.0, 0.0, 3.94, 0.13, 64.42, 1014.68, 10.26))
    return render_template('city.html', results=newArr)

@app.route('/<path:filename>')
def sendfile(filename):
    return send_from_directory(app.static_folder, filename)
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('homePage.html')
if (__name__ == '__main__'):
    app.run(debug=True)
