import functions

startdate = '2020-03-01'
ts_startdate = functions.get_timestamp(startdate)

enddate = '2021-08-01'
ts_enddate = functions.get_timestamp(enddate)

btcdict = functions.get_btc_data(ts_startdate, ts_enddate, startdate)

functions.get_variables(btcdict)