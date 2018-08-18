import requests # Make sure to do pip install requests
import json
import config # Make your own config.py file to place you api key into
import time
import csv

API_KEY = "724372896dda4401acf181258182607"
API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"
DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class Weather:
    def __init__(self, date, city, state, avgHigh, avgLow, uvIndex, totalSunHours, avgSunHours, totalSnow, avgSnow, totalRainfall, avgRainfall, avgHumidity, avgPressure, avgWindSpeed):
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


def get_api_count():
    file = open("api_count.txt", "r")
    api_count = file.readline()
    file.close()
    return int(api_count)

# Checks to see if the year specified is a leap year or not.
def isLeapYear(year):
    tempYear = year - 2000
    if (tempYear % 4 == 0):
        return True

    return False
# Gets the last day of the month
def getEndDate(month, year):
    if (month == 2 and isLeapYear(year)):
        endDate = "{}/{}/29".format(year, month)
    else:
        endDate = "{}/{}/{}".format(year, month, DAYS[month - 1])

    return endDate

#Creates a new weather object
def createNewWeather(response, month, year, city, state):
    avgHigh = 0
    avgLow = 0
    avgSun = 0
    avgUV = 0
    avgSnow = 0
    avgRainfall = 0
    avgHumidity = 0
    avgPressure = 0
    avgWindSpeed = 0

    totalHigh = 0
    totalLow = 0
    totalUV = 0
    totalSun = 0
    totalSnow = 0
    totalRainfall = 0
    totalHumidity = 0
    totalPressure = 0
    totalWindSpeed = 0
    numOfDays = 0

    for i in response['data']['weather']:
        totalHigh += int(i['maxtempF'])
        totalLow += int(i['mintempF'])
        totalUV += int(i['uvIndex'])
        totalSun += float(i['sunHour'])
        totalSnow += float(i['totalSnow_cm'])
        totalRainfall += float(i['hourly'][0]['precipMM'])
        totalHumidity += int(i['hourly'][0]['humidity'])
        totalPressure += int(i['hourly'][0]['pressure'])
        totalWindSpeed += int(i['hourly'][0]['WindGustMiles'])
        numOfDays += 1
        
    totalRainfall = round(totalRainfall * 0.0393701, 2)
    avgHigh = round(totalHigh / numOfDays, 2)
    avgLow = round(totalLow / numOfDays, 2)
    avgSnow = round(totalSnow / numOfDays, 2)
    avgSun = round(totalSun / numOfDays, 2)
    avgUV = round(totalUV / numOfDays, 2)
    avgRainfall = round(totalRainfall / numOfDays, 2)
    avgHumidity = round(totalHumidity / numOfDays, 2)
    avgPressure = round(totalPressure / numOfDays, 2)
    avgWindSpeed = round(totalWindSpeed / numOfDays, 2)
    totalSun = round(totalSun, 2)
    totalSnow = round(totalSnow, 2)

    date = "{}/{}".format(year, month)

    return Weather(date, city, state, avgHigh, avgLow, avgUV, totalSun, avgSun, totalSnow, avgSnow, totalRainfall, avgRainfall, avgHumidity, avgPressure, avgWindSpeed)

# Gets the city and state name of the index specified
def getCitiesAndStates(CITIES, STATES, indexStart, indexEnd):
    if (indexStart == 0):
        indexStart = 1

    with open('locations.csv', 'r', encoding="utf8") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if (i >= indexStart and i <= indexEnd):
                CITIES.append(row[1])
                STATES.append(row[2])
            i += 1

def main():
    CITIES = []
    STATES = []

    print("\nMake sure to enter index as if you were accessing data in an array by it's index. arr[0] is 1st element.")
    indexStart = int(input("Starting city index (0, 100, 200): "))
    currentIndex = indexStart
    print("\nWe are limited to retrieving a years worth of data for 38 cities every day.")
    print("If your start index is 0, make your end index 38")
    indexEnd = int(input("Ending city index: "))

    # getCitiesAndStates(CITIES, STATES, indexStart, indexEnd)

    cityCount = 0
    while (cityCount < (indexEnd - indexStart)):
        month = 5
        year = 2018
        city = "Newport" # Medford, Bend, Newport
        state = "Oregon"

        while ("{}/{}".format(year, month) != "2018/7"):
            if (month == 13):
                month = 1
                year += 1

            parameters = {
                "q": "{}, {}".format(city, state),
                "key": API_KEY,
                "date": "{}/{}/01".format(year, month),
                "enddate": getEndDate(month, year),
                "tp": "24",
                "format": "json"
            }
            response = requests.get(API_ENDPOINT, params=parameters)

            if (response.status_code != 200):
                print("Bad response from API. You have most likely reached your limit for the day.")
                return
            else:
                print("Successful response from API on date: {}/{} | index: {} | {}, {}".format(year, month, currentIndex, city, state), flush=True)

            data = json.loads(response.content)
            w = createNewWeather(data, month, year, city, state)

            file = open("./weather_data/weather-data-complete.csv", "a")
            file.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(308 + currentIndex, w.city, w.state, w.date, w.avgHigh, w.avgLow, w.uvIndex, w.totalSunHours, w.avgSunHours, w.totalSnow, w.avgSnow, w.totalRainfall, w.avgRainfall, w.avgHumidity, w.avgPressure, w.avgWindSpeed))
            file.close()
        
            month += 1
            time.sleep(2)
        currentIndex += 1
        cityCount += 1
    
if __name__ == '__main__':
    main()