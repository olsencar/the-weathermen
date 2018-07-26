import requests # Make sure to do pip install requests
import json
import config # Make your own config.py file to place you api key into
import time
import csv

API_KEY = config.api_key
API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class Weather:
    def __init__(self, date, city, state, avgHigh, avgLow, uvIndex, totalSunHours, avgSunHours, totalSnow, avgSnow):
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

def get_api_count():
    file = open("api_count.txt", "r")
    api_count = file.readline()
    file.close()
    return int(api_count)

def isLeapYear(year):
    tempYear = year - 2000
    if (tempYear % 4 == 0):
        return True

    return False

def getEndDate(month, year):
    if (month == 2 and isLeapYear(year)):
        endDate = "{}/{}/29".format(year, month)
    else:
        endDate = "{}/{}/{}".format(year, month, DAYS[month - 1])

    return endDate

def createNewWeather(response, month, year, city, state):
    avgHigh = 0
    avgLow = 0
    avgSun = 0
    avgUV = 0
    avgSnow = 0
    
    totalHigh = 0
    totalLow = 0
    totalUV = 0
    totalSun = 0
    totalSnow = 0
    numOfDays = 0

    for i in response['data']['weather']:
        totalHigh += int(i['maxtempF'])
        totalLow += int(i['mintempF'])
        totalUV += int(i['uvIndex'])
        totalSun += float(i['sunHour'])
        totalSnow += float(i['totalSnow_cm'])
        numOfDays += 1

    avgHigh = round(totalHigh / numOfDays, 2)
    avgLow = round(totalLow / numOfDays, 2)
    avgSnow = round(totalSnow / numOfDays, 2)
    avgSun = round(totalSun / numOfDays, 2)
    avgUV = round(totalUV / numOfDays, 2)
    totalSun = round(totalSun, 2)
    totalSnow = round(totalSnow, 2)

    date = "{}/{}".format(year, month)

    return Weather(date, city, state, avgHigh, avgLow, avgUV, totalSun, avgSun, totalSnow, avgSnow)

def getCitiesAndStates(CITIES, STATES, indexStart, indexEnd):
    if (indexStart == 0):
        indexStart = 1

    with open('locations.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if (i >= indexStart and i < indexEnd):
                CITIES.append(row[1])
                STATES.append(row[2])
            i += 1

def main():
    CITIES = []
    STATES = []

    print("\nMake sure to ender index as if you were accessing data in an array by it's index. arr[0] is 1st element.")
    indexStart = int(input("Starting city index (0, 100, 200): "))

    print("\nWe are limited to retrieving a years worth of data for 39 cities every day.")
    print("If your start index is 0, make your end index 39")
    indexEnd = int(input("Ending city index: "))

    getCitiesAndStates(CITIES, STATES, indexStart, indexEnd)

    cityCount = 0
    while (cityCount < 39):
        month = 6
        year = 2017
        city = CITIES[cityCount]
        state = STATES[cityCount]
        while ("{}/{}".format(year, month) != "2018/7"):
            if (month == 13):
                month = 1
                year += 1

            parameters = {
                "q": "{}, {}".format(city, state),
                "key": API_KEY,
                "date": "{}/{}/01".format(year, month),
                "enddate": getEndDate(month, year),
                "format": "json"
            }
            response = requests.get(API_ENDPOINT, params=parameters)

            if (response.status_code != 200):
                print("Bad response from API. You have most likely reached your limit for the day.")
                return
            else:
                print("Successful response from API on date: {}/{} | index: {} | {}, {}".format(year, month, indexStart, city, state), flush=True)

            data = json.loads(response.content)
            w = createNewWeather(data, month, year, city, state)

            file = open("weather-data.csv", "a")
            file.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(indexStart, w.city, w.state, w.date, w.avgHigh, w.avgLow, w.uvIndex, w.totalSunHours, w.avgSunHours, w.totalSnow, w.avgSnow))
            file.close()
        
            month += 1
            time.sleep(2)
        indexStart += 1
        cityCount += 1
    
if __name__ == '__main__':
    main()