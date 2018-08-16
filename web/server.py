from flask import Flask, render_template, url_for, request, send_from_directory
from datetime import datetime
import json
import re
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

def querySearch(searchTerm, city, state, beginDate, endDate, minTemp, maxTemp, minRain, maxRain):
    searchTerm = re.sub('[^A-Za-z, ]+', '', searchTerm)
    print(searchTerm)
    splitSearch = searchTerm.split(',')
    searchTerm1 = searchTerm
    if (len(splitSearch) > 1):
        splitSearch[0].strip()
        splitSearch[1].strip()
        searchTerm = "'{}' AND '{}')".format(splitSearch[0], splitSearch[1])
        searchTerm1 = searchTerm

    if (minRain == '' or minRain == None):
        minRain = 0
    if (maxRain == '' or maxRain == None):
        maxRain = 1000

    if (beginDate == ''):
        beginDate = "2017-6"
    searchTerm += " [{} to ".format(beginDate)

    if (endDate == ''):
        endDate = "2018-6"
    searchTerm += "{}] ".format(endDate)

    if (minTemp == '' or minTemp == None):
        minTemp = "-80"

    if (maxTemp == '' or maxTemp == None):
        maxTemp = "140"

    cityState = "{}, {}".format(city, state)
    print("searchterm: {}".format(searchTerm))
    with indexer.searcher() as searcher:
        print("MIN RAIN", minRain)
        queryTest = MultifieldParser(["City", "avgTemp", "avgLow", "avgHigh", "State", "Date"], schema=indexer.schema).parse(searchTerm)
        np = NumericRange("avgTemp", float(minTemp), float(maxTemp))
        nr = NumericRange("avgRainfall", float(minRain), float(maxRain))
        
        query2 = MultifieldParser(["City", "avgTemp", "State", "Date", "avgRainfall"], schema=indexer.schema).parse(searchTerm1)

        tempResults = searcher.search(query2, filter=np, limit=None)
        rainResults = searcher.search(query2, filter=nr, limit=None)
        results = searcher.search(queryTest, limit=None)
        results.filter(tempResults)
        results.filter(rainResults)
        print("LENGTH: of results", len(results))

        arr = []
        Cities = []

        for line in results:
            found = False
            if (len(Cities) == 0):
                Cities.append([line['City'], line['State'], line['avgLow'], line['avgHigh']])
            else:
                for i in Cities:
                    if (line['City'].lower() == i[0].lower() and line['State'].lower() == i[1].lower()):
                        found = True
                        break
                if (not found):
                    Cities.append([line['City'], line['State'], line['avgLow'], line['avgHigh']])    
            arr.append(City(line['City'], line['State'], datetime.strftime(line['Date'], "%Y-%m"), line['avgHigh'], line['avgLow'],line['avgUV'], line['totalSun'], line['avgSun'],line['totalSnow'], line['avgSnow'], line['totalRainfall'], line['avgRainfall'], line['avgHumidity'], line['pressure'], line['windSpeed'], line['avgTemp']))
        for key in Cities:
            print("City: " + key[0] + " State: " + key[1]);
    return results, Cities, arr

@app.route('/results', methods=['GET', 'POST'])
def results():
    data = request.args
    print(data)
    query = data.get('searchterm')
    cityName = data.get('city')
    stateName = data.get('state')
    minRain = data.get('minRain')
    maxRain = data.get('maxRain')
    minTemp = data.get('minTemp')
    maxTemp = data.get('maxTemp')
    beginDate = data.get('beginDate')
    endDate = data.get('endDate')

    searchTerm = query
    latnlon = ""
    results, Cities, arr = querySearch(searchTerm, cityName, stateName, beginDate, endDate, minTemp, maxTemp, minRain, maxRain)
    fp = open("../locations.csv", "r");
    for line in fp:
        splitL = line.split(',')
        temp = [splitL[1],splitL[2], splitL[3], splitL[4].strip('\n')]
        for i in Cities:
            if (i[0].lower() == splitL[1].lower() and i[1].lower() == splitL[2].lower()):
                latnlon += "{},{},{},{},{},{},".format(temp[0], temp[1], temp[2], temp[3], i[2], i[3])
                break;

    fp.close()
    print("You searched for: " + query)
    if (len(Cities) > 1):
        return render_template('results.html', latnlon=latnlon, query=query, results=Cities, result2=arr, searchterm=searchTerm, minTemp=minTemp, maxTemp=maxTemp, minRain=minRain, maxRain=maxRain, beginDate=beginDate, endDate=endDate)
    elif (len(Cities) == 0):
        return render_template('error.html')
    else:
        return render_template('city.html', latnlon=latnlon, results=arr)


@app.route('/city', methods=['GET'])
def city():
    data = request.args
    print(data)
    minRain = data.get('minRain')
    maxRain = data.get('maxRain')
    cityName = data.get('city')
    stateName = data.get('state')
    minTemp = data.get('minTemp')
    maxTemp = data.get('maxTemp')
    beginDate = data.get('beginDate')
    endDate = data.get('endDate')

    searchTerm = data.get('searchterm')

    Cities = []
    arr = []
    latnlon = ""
    newArr = []
    results, Cities, arr = querySearch(searchTerm, cityName, stateName, beginDate, endDate, minTemp, maxTemp, minRain, maxRain)

    if (len(Cities) > 1):
        for i in arr:
            if (i.city.lower() == cityName.lower() and i.state.lower() == stateName.lower()):
                newArr.append(i)
    else:
        newArr = arr
    fp = open("../locations.csv", "r");
    for line in fp:
        splitL = line.split(',')
        temp = [splitL[1],splitL[2], splitL[3], splitL[4].strip('\n')]
        if (splitL[1] == newArr[0].city and splitL[2] == newArr[0].state):
            print("{} = {}".format(i, splitL[1]))
            latnlon += "{},{},{},{},{},{}".format(temp[0], temp[1], temp[2], temp[3], newArr[0].avgLow, newArr[0].avgHigh)
            break
    latnlon = latnlon[:-1]

    fp.close()

    print(searchTerm)
    print("IN CITIES")
    return render_template('city.html', latnlon=latnlon, results=newArr)

@app.route('/<path:filename>')
def sendfile(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/', methods=['GET', 'POST'])
def home():
    results, Cities, arr = querySearch("",'','', '', '', '', '', '', '')
    fp = open("../locations.csv", "r");
    latnlon = ""
    for line in fp:
        splitL = line.split(',')
        temp = [splitL[1],splitL[2], splitL[3], splitL[4].strip('\n')]
        for i in Cities:
            if (i[0] == splitL[1]):
                print("{} = {}".format(i, splitL[1]))
                print(temp)
                latnlon += "{},{},{},{},{},{},".format(temp[0], temp[1], temp[2], temp[3], i[2], i[3])
                break
    latnlon = latnlon[:-1]
    fp.close()
    return render_template('homePage.html', latnlon=latnlon, results=arr)

if (__name__ == '__main__'):
    app.run(debug=True)
