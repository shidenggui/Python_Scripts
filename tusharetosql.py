import threading
import tushare as ts
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine

stock_basic = ts.get_stock_basics()

stock_timetomarket = stock_basic['timeToMarket']

stock_timetomarket = stock_timetomarket.map(lambda x: dt.datetime.strptime(str(x), '%Y%m%d').strftime('%Y-%m-%d'))

stock_timetomarket.order(ascending=False, inplace=True)
#stock_timetomarket.order(ascending=True, inplace=True)

engine = create_engine('mysql://root:root@127.0.0.1/tushare?charset=utf8')


index = 0
max = len(stock_timetomarket.index)
lock = threading.Lock()

def getdata(code):
	global lock
	dayhistory = ts.get_h_data(code, stock_timetomarket[code])
	if not dayhistory:
		dayhistory = ts.get_h_data(code, stock_timetomarket[code], index=True)
	dayhistory['code'] = code
	dayhistory.index = dayhistory.index.date
	print '\n code %s insert......\n' % code
	dayhistory.to_sql('h_data', engine, if_exists='append')

def getdatathread():
	global index
	while index < max:
		print index
		index += 1
		indexbak = index - 1
		code = stock_timetomarket.index[indexbak]
		print 'start: ', code
		dayhistory = ts.get_h_data(code, stock_timetomarket[code])
		dayhistory['code'] = code
		dayhistory.index = dayhistory.index.date
		print '\n code %s insert......\n' % code
		dayhistory.to_sql('h_data', engine, if_exists='append')

for x in xrange(3):
	thread = threading.Thread(target=getdatathread)
	thread.start()



