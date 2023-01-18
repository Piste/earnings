from flask import Flask
from flask import request
from io import BytesIO
import requests
import time
import pandas as pd
import csv
import os

def earnings_calendar_api(api_key, horizon, symbol=None):
    if symbol is not None:
        url = f'{BASE_URL}function=EARNINGS_CALENDAR&symbol={symbol}&horizon={horizon}&apikey={api_key}'
        response = requests.get(url)
    else:
        url = f"{BASE_URL}function=EARNINGS_CALENDAR&horizon={horizon}&apikey={api_key}"
        response = requests.get(url)

    return pd.read_csv(BytesIO(response.content))

API_KEY = os.getenv('ALPHA_VANTAGE_KEY')
horizon=["3month","6month","12month"]
BASE_URL = "https://www.alphavantage.co/query?"

app = Flask(__name__)

res = earnings_calendar_api(API_KEY,horizon[0])
print ("Earnings loaded")
print (res)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/earnings')
def earnings():
    ticker = request.args.get('ticker') 
    if ticker:
        earnings_date = res[res.symbol==ticker]['reportDate'].values[0]
        print(f"earnings_date: {earnings_date}")
        return earnings_date
    return 

if __name__ == '__main__':
  app.run(port=8000, host='0.0.0.0', debug=True)
