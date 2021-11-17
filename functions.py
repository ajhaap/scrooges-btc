import json
import requests
from datetime import datetime

def get_timestamp(date):

    string = f'{date} 01:00:00.000000 +0000'
    date_time = datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f %z")
    timestamp = datetime.timestamp(date_time)

    return int(timestamp)

def get_btc_data(ts_startdate, ts_enddate):

    if (ts_enddate - ts_startdate) < 7776001:
        ts_startdate = int(ts_enddate - 7776001)

    r = requests.get(
        f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=eur&from={ts_startdate}&to={ts_enddate}',
        )

    data = json.loads(r.content)

    prices = [x[1] for x in data['prices']]
    dates = [x[0] for x in data['prices']]
    volumes = [x[1] for x in data['total_volumes']]
    utcdates = []

    for date in dates:
        timestamp = date / 1000
        utcdate = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        utcdates.append(utcdate)

    btcdict = [{'date': utcdate, 'price': price, 'volume': volume}
               for utcdate,price,volume in zip(utcdates,prices,volumes)]

    return btcdict


