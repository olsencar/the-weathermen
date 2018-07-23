API_KEY = "7826c9f4779b4375b89185008181207"
API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"

import requests # Make sure to do pip install requests
import json
from pprint import pprint # make sure to do pip install pprint

parameters = {
    "q": "Corvallis",
    "key": API_KEY,
    "date": "2009/06/1",
    "format": "json"
}
r = json.loads(requests.get(API_ENDPOINT, params=parameters).content)
# result = json.loads(r.content)


pprint(r['data']['weather'])
