import json
import requests
from datetime import datetime, timezone

timestring = ' 01:00:00.000000 +0000'
timeformat = '%Y-%m-%d %H:%M:%S.%f %z'

def vali_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise Exception("Incorrect format. Format should be YYYY-MM-DD") from None

    date = datetime.strptime(f'{date}{timestring}', f'{timeformat}')

    return date


def check_dates(startdate, enddate):

    enddate = vali_date(enddate)
    startdate = vali_date(startdate)

    first_date = datetime.strptime(f'2012-11-25 17:18:45.000000 +0000',
                                   f'{timeformat}')
    today = datetime.now(timezone.utc)

    if startdate < first_date:
        startdate = first_date

    if startdate > enddate:
        raise Exception("Start date cannot be higher than end date. Support for space-time folding"
                     " will be added in version 2.0")

    if enddate > today:
        raise Exception("You cannot get data from the future you silly goo.. err.. duck")

    return True

def get_timestamp(date):

    string = f'{date}{timestring}'
    date_time = datetime.strptime(string, timeformat)
    timestamp = datetime.timestamp(date_time)

    return int(timestamp)


def get_btc_data(ts_startdate, ts_enddate):

    r = requests.get(
        f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
        f'/range?vs_currency=eur&from={ts_startdate}&to={ts_enddate}'
        )

    data = json.loads(r.content)

    return data


def parse_data(startdate, enddate):

    date_index = False

    ts_startdate = get_timestamp(startdate)
    ts_enddate = get_timestamp(enddate)

    data = get_btc_data(ts_startdate, ts_enddate)

    if (ts_enddate - ts_startdate) < 7776001:
        ts_startdate = int(ts_enddate - 7776001)
        date_index = True

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

    return utcdates, prices, volumes


def get_variables(startdate, enddate):

    check_dates(startdate, enddate)

    utcdates, prices, volumes = parse_data(startdate, enddate)

    max_price = prices[0]
    current_price = max_price
    min_price = 0
    min_index, max_index = 1, 0
    profit = 0
    index = -1
    """nimeä nämä uudelleen"""
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
        highest = max(volumes)
        buyorsell = (utcdates[min_index], utcdates[max_index])

    results = {'bearish': bearish, 'highest': highest, 'buyorsell': buyorsell}

    return results