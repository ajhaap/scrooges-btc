import json

import arrow

from datetime import datetime

from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

"""Get the start and end days from user. Set the day's timestamp to 01:00 and get the timecode for that time"""
startdate = input("Start date: ")
startdate = arrow.get(f'{startdate} 01:00:00', 'YYYY-MM-DD hh:mm:ss')
ts_startdate = startdate.timestamp()

enddate = input("End date: ")
enddate = arrow.get(f'{enddate} 01:00:00', 'YYYY-MM-DD hh:mm:ss')
ts_enddate = enddate.timestamp()

"""
If the the time between start and end date is less than 90 days, add 90 days
CoinGeckoAPI returns only daily values from 00:00 when the request is for 90+ days.
We do this in order to get a tidier list
"""

if (ts_enddate - ts_startdate) < 7776000:
    ts_startdate = int(ts_enddate - 7776000)

price = cg.get_coin_market_chart_range_by_id('bitcoin', 'eur', ts_startdate, ts_enddate)

"""Parse into a dictionary"""

pricedict = {}

for x in price['prices']:
    timestamp = int(x[0]) / 1000
    utcdate = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
    pricedict.update({utcdate: x[1]})

for item in pricedict.items():
    print(item)



