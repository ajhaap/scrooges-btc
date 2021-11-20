import functions

startdate = '2005-01-19'
ts_startdate = functions.get_timestamp(startdate)

enddate = '2021-11-20'
ts_enddate = functions.get_timestamp(enddate)

btcdict = functions.get_btc_data(ts_startdate, ts_enddate, startdate)

functions.get_variables(btcdict)