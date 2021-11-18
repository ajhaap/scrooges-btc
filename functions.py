import json
import requests
from datetime import datetime


def get_timestamp(date):

    string = f'{date} 01:00:00.000000 +0000'
    date_time = datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f %z")
    timestamp = datetime.timestamp(date_time)

    return int(timestamp)


def get_btc_data(ts_startdate, ts_enddate, startdate):

    date_index = False
    list_index = ''

    if (ts_enddate - ts_startdate) < 7776001:
        ts_startdate = int(ts_enddate - 7776001)
        date_index = True

    r = requests.get(
        f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
        f'/range?vs_currency=eur&from={ts_startdate}&to={ts_enddate}'
        )

    data = json.loads(r.content)

    dates = [x[0] for x in data['prices']]
    utcdates = []

    for date in dates:
        timestamp = date / 1000
        utcdate = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        utcdates.append(utcdate)

    if date_index:
        list_index = utcdates.index(str(startdate))
        utcdates = utcdates[list_index:]

    prices = [x[1] for x in data['prices']]
    if date_index:
        prices = prices[list_index:]

    volumes = [x[1] for x in data['total_volumes']]
    if date_index:
        volumes = volumes[list_index:]

    keys = ['date', 'price', 'volume']
    values = [utcdates, prices, volumes]
    btcdict = dict(zip(keys, values))

    return btcdict


def get_variables(dictionary):
    tobuy_date, tosell_date = '', ''
    highest = max(dictionary['volume'])
    max_price = dictionary['price'][0]
    min_price = max_price
    profit = 0
    min_index, max_index = 0, 0

    index = 0
    for x in dictionary['price']:
        index += 1
        if x - min_price > profit and x > min_price:
            profit = x - min_price
            max_index = index
        if x < min_price:
            min_index = index
            min_price = x

    tobuy_date = dictionary['date'][min_index]
    tosell_date = dictionary['date'][max_index]

    return print(f'Hightest volume was on {highest}\n'
                 f'For maximum profits, one should buy on {tobuy_date}'
                 f' and sell on {tosell_date}')
