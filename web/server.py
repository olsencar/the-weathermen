from flask import Flask, render_template, url_for, request, send_from_directory, Response
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
import requests
from datetime import datetime

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

class ApixuException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        message = 'Error code %s: "%s"' % (code, message)
        super(ApixuException, self).__init__(message)

class ApixuClient:
    def __init__(self, api_key="66a28df2262b4cf4a99230248182708", host_url='http://api.apixu.com'):
        self.api_key = api_key
        self.host_url = host_url.rstrip('/')

    def _get(self, url, args=None):
        new_args = {}
        if self.api_key:
            new_args['key'] = self.api_key
        new_args.update(args or {})
        response = requests.get(url, params=new_args)
        json_res = response.json()
        if 'error' in json_res:
            err_msg = json_res['error'].get('message')
            err_code = json_res['error'].get('code')
            raise ApixuException(message=err_msg, code=err_code)

        return json_res

    def getCurrentWeather(self, q=None):
        url = '%s/v1/current.json' % self.host_url
        args = {}
        if q:
            args['q'] = q

        return self._get(url, args)

    def getForecastWeather(self, q=None, days=None):
        url = '%s/v1/forecast.json' % self.host_url
        args = {}
        if q:
            args['q'] = q
        if days:
            args['days'] = days

        return self._get(url, args)
weather = ApixuClient()
def findMatch(search):
    with open('../variations.txt', 'r') as file:
        complete = ""
        found = False
        for line in file:
            lineSplit = line.split(',')
            for i in lineSplit:
                if (i == search):
                    found = True
                    complete += "{},".format(lineSplit[0])
        if (not found):
            complete = "-1"
        else:
            complete = complete[:-1]
    return complete

def querySearch(searchTerm, city, state, beginDate, endDate, minTemp, maxTemp, minRain, maxRain):
    searchTerm = re.sub('[^A-Za-z, ]+', '', searchTerm)
    searchTermTemp = searchTerm.lower().split(',')
    
    cityState = False
    searchTermTemp[0] = searchTermTemp[0].strip()
    if (len(searchTermTemp) > 1):
        cityState = True
        searchTermTemp[1] = searchTermTemp[1].strip()

    print("IN query:", searchTerm)
    with open('../variations.txt', 'r') as file:
        for line in file:
            lineSplit = line.split(',')
            found = False
            for i in lineSplit:
                if (cityState):
                    if (i == searchTermTemp[1]):
                        found = True
                        searchTermTemp[1] = lineSplit[0]
                        break
                else:
                    if (i == searchTermTemp[0]):
                        found = True
                        searchTermTemp[0] = lineSplit[0]
                        break
            if (found):
                break

    splitSearch = searchTermTemp
    searchTerm1 = searchTerm
    if (cityState):
        searchTerm = "'{}' AND '{}')".format(splitSearch[0], splitSearch[1])
    else:
        searchTerm = splitSearch[0]
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
    
    with indexer.searcher() as searcher:
        queryTest = MultifieldParser(["City", "State", "Date"], schema=indexer.schema).parse(searchTerm)
        
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
                if (cityState):
                    if (line['City'].lower().strip() == splitSearch[0].lower() and line['State'].lower() == splitSearch[1].lower()):
                        Cities.append([line['City'], line['State'], line['avgLow'], line['avgHigh']])
                else:
                    Cities.append([line['City'], line['State'], line['avgLow'], line['avgHigh']])
            else:
                for i in Cities:
                    if (line['City'].lower() == i[0].lower() and line['State'].lower() == i[1].lower()):
                        found = True
                        break
                if (not found):
                    if (cityState):
                        if (line['City'].lower() == splitSearch[0].lower() and line['State'].lower() == splitSearch[1].lower()):
                            Cities.append([line['City'], line['State'], line['avgLow'], line['avgHigh']])   
                    else:
                        Cities.append([line['City'], line['State'], line['avgLow'], line['avgHigh']])
            arr.append(City(line['City'], line['State'], datetime.strftime(line['Date'], "%Y-%m"), line['avgHigh'], line['avgLow'],line['avgUV'], line['totalSun'], line['avgSun'],line['totalSnow'], line['avgSnow'], line['totalRainfall'], line['avgRainfall'], line['avgHumidity'], line['pressure'], line['windSpeed'], line['avgTemp']))
    print(Cities)
    print(cityState)
    return results, Cities, arr

@app.route('/search', methods=['GET', 'POST'])
def search():
    data = request.args
    query = data.get('val')
    resp = findMatch(query)
    return Response(resp, status=200, mimetype="text/plain")


@app.route('/results', methods=['GET', 'POST'])
def results():
    data = request.args
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
        return render_template('results.html', latnlon=latnlon, query=query, results=Cities, result2=arr, searchterm=searchTerm, minTemp=minTemp, maxTemp=maxTemp, beginDate=beginDate, endDate=endDate, minRain=minRain, maxRain=maxRain)
    elif (len(Cities) == 0):
        return render_template('error.html', query=query)
    else:
        latlon = latnlon.split(',')
        data = weather.getForecastWeather(q="{},{}".format(latlon[2], latlon[3]), days=6)
        for item in data['forecast']['forecastday']:
            date = datetime.strptime(item['date'], "%Y-%m-%d")
            item['date'] = datetime.strftime(date, "%a, %b %d")
        return render_template('city.html', latnlon=latnlon, results=arr, forecast=data)


@app.route('/city', methods=['GET', 'POST'])
def city():
    data = request.args
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
            latnlon += "{},{},{},{},{},{}".format(temp[0], temp[1], temp[2], temp[3], newArr[0].avgLow, newArr[0].avgHigh)
            break
    latnlon = latnlon[:-1]

    fp.close()

    latlon = latnlon.split(',')
    data = weather.getForecastWeather(q="{},{}".format(latlon[2], latlon[3]), days=6)
    
    for item in data['forecast']['forecastday']:
        date = datetime.strptime(item['date'], "%Y-%m-%d")
        item['date'] = datetime.strftime(date, "%a, %b %d")
    return render_template('city.html', latnlon=latnlon, results=newArr, forecast=data)

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
                latnlon += "{},{},{},{},{},{},".format(temp[0], temp[1], temp[2], temp[3], i[2], i[3])
                break
    latnlon = latnlon[:-1]
    fp.close()
    return render_template('homePage.html', latnlon=latnlon, results=arr)

if (__name__ == '__main__'):
    app.run(debug=True)
