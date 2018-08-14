from flask import Flask, render_template, url_for, request, send_from_directory
from datetime import datetime

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
<<<<<<< HEAD
    if (request.method == 'POST'):
        data = request.form
    else:
        data = request.args

    results = ["Portland", "Corvallis", "New York", "Chicago"]
    query = data.get('searchterm').title()
=======
    data = request.args
    query = data.get('searchterm')
    
>>>>>>> 7cd8dba53ff6d0918b8d91cd2789c2dc6f88317b
    beginDate = data.get('beginDate')
    endDate = data.get('endDate')

    if (beginDate != ''):
        beginDate = datetime.strptime(beginDate, "%Y-%m")
    
    if (endDate != ''):
        endDate = datetime.strptime(endDate, "%Y-%m")

    minTemp = int(data.get('minTemp'))
    maxTemp = int(data.get('maxTemp'))
    # SHANE ENTER YOUR WHOOSH INDEX HERE
    # FOR the begin dates and end dates, first check if = '', then use strftime(date, "%Y-%m")

    
    print("You searched for: " + query)
    return render_template('results.html', query=query)

@app.route('/city/', methods=['GET', 'POST'])
def city():
    data = request.args

    cityName = data.get('city')
    stateName = data.get('state')

    # Get data about city from query
    city = []
    city.append(City("New York","New York","2017/7",88.48,77.0,0.0,0.0,0.0,0.0,0.0,3.94,0.13,64.42,1014.68,10.26))
    city.append(City("New York","New York","2017/8",88.48,77.0,0.0,0.0,0.0,0.0,0.0,3.94,0.13,64.42,1014.68,10.26))
    return render_template('city.html', city=city)
if (__name__ == '__main__'):
    app.run(debug=True)
