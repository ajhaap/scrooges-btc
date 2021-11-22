import json
import requests
from datetime import datetime


def get_timestamp(date):

    string = f'{date} 01:00:00.000000 +0000'
    date_time = datetime.strptime(string, "%Y-%m-%d %H:%M:%S.%f %z")
    timestamp = datetime.timestamp(date_time)

    return int(timestamp)


def get_btc_data(startdate, enddate):

    ts_startdate = get_timestamp(startdate)
    ts_enddate = get_timestamp(enddate)

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

    highest = max(volumes)

    max_price = prices[0]
    current_price = max_price
    min_price = 0
    min_index, max_index = 1, 0
    profit = 0
    index = -1

    bearish, current_bearish = 0, 0

    for price in prices:
        """The following gets the days to buy and sell for best profit"""
        index += 1

        if price < min_price:
            min_index = index
            min_price = price

        if price - min_price > profit and price > min_price:
            profit = price - min_price
            max_index = index
            max_price = price
        """The following gets the longest downward (bearish) trend in prices"""
        if price - current_price < 0:
            current_bearish += 1
            if current_bearish > bearish:
                bearish = current_bearish

        if price - current_price > 0:
            if current_bearish > bearish:
                current_bearish = bearish
            current_bearish = 0

        current_price = price

    if min_index == max_index:
        buyorsell = None
    else:
        buyorsell = (utcdates[min_index], utcdates[max_index])

    results = {'bearish': bearish, 'highest': highest, 'buyorsell': buyorsell}

    return results