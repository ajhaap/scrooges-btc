import functions

startdate = '2021-11-11'
ts_startdate = functions.get_timestamp(startdate)

enddate = '2021-11-15'
ts_enddate = functions.get_timestamp(enddate)

btcdict = {}

list = functions.get_btc_data(ts_startdate, ts_enddate)

print(list)








