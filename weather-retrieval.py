API_KEY = "7826c9f4779b4375b89185008181207"
API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"

import requests
import json

parameters = {
    "q": "Corvallis",
    "key": API_KEY,
    "date": "2009/06/1",
    "enddate": "2009/06/30",
    "format": "json"
}
response = requests.get(API_ENDPOINT, params=parameters)
print(response.content)