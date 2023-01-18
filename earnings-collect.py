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
tickers=["AAPL", "UNH"]

def ext_tickdate(headed_df):
    # print(headed_df.loc[1, 'symbol'])
    # print(headed_df.head(10))
    symbol = headed_df["symbol"].values[0]
    reportDate = headed_df["reportDate"].values[0]
    print(f"", symbol, "\t", reportDate)
    return symbol, reportDate

tickdate = {}

for i in tickers:
    res = earnings_calendar_api(API_KEY,horizon[0],i)
    s, r = ext_tickdate(res)
    tickdate[s] = r
    # print(res)

print(tickdate)
