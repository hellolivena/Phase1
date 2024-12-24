# %%
##REGULAR IMPORTS

import os
import time
import datetime
from datetime import datetime
import traceback
import talib
import pandas as pd
from Ayush_lib import CLASS_AYUSH
from dhanhq import dhanhq
import pandas as pd
from datetime import date,datetime, timedelta, timezone
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf

dir(talib)

#talib functions complete export
abc =dict(talib.get_function_groups())
abc_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in abc.items()]))
# abc_df.to_excel('talib.xlsx',index = 'False')

# print(help(talib))


#dhanlib
client_code="1102634633"
token_id="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM2MzY5ODQ1LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMjYzNDYzMyJ9.bJ2qnpR8efbHENikiCJiaMbJH-tBfCKY8__HCFuroCsNk_aj_HWMrBqu65BynCDlKQlbY-47-vYHboZtrBBVHQ"

# %%
###HISTORICAL DATA 3 YEAR. CANDLE RSI EMA CHARTING


dhan1=dhanhq(client_code,token_id)
securityId="13"
exchangeSegment="IDX_I"
instrument="INDEX"
expiryCode= 0
fromDate="2022-01-01"
toDate="2024-12-26"
interval=5

1
hist_data=dhan1.historical_daily_data(securityId,exchangeSegment,instrument,fromDate,toDate,expiryCode)
hist_data1=pd.DataFrame(hist_data['data'])
hist_data1 = hist_data1.sort_index()
hist_data1['DATET'] = pd.to_datetime(hist_data1['timestamp'],unit = 's',utc=True).dt.tz_convert('Asia/Kolkata').dt.date
hist_data1['DATET'] = pd.to_datetime(hist_data1['DATET'])
# hist_data1['EMA10'] = talib.EMA(hist_data1['close'], timeperiod=10)
hist_data1['EMA20'] = talib.EMA(hist_data1['close'], timeperiod=20)
# hist_data1['EMA50'] = talib.EMA(hist_data1['close'], timeperiod=50)
hist_data1['EMA200'] = talib.EMA(hist_data1['close'], timeperiod=200)
# hist_data1["EMA200PD"] = hist_data1.close.ewm(span=200,adjust=False,min_periods=200).mean()
hist_data1["RSI14"] = talib.RSI(hist_data1['close'],timeperiod = 14)
print(hist_data1['DATET'])
# print(hist_data1[['EMA200PD','EMA200','RSI14']])
hist_data1.set_index('DATET', inplace=True)


ema_plot = mpf.make_addplot(hist_data1['EMA20'])
rsi_plot = mpf.make_addplot(hist_data1['RSI14'],panel=1, color='green', title='RSI 14')
mpf.plot(hist_data1, type='candle', style='charles', title="Candlestick Chart", ylabel='Price',addplot=[mpf.make_addplot(hist_data1[['EMA200','EMA20']]),rsi_plot],figsize=(10, 8), panel_ratios=(4,1))

# hist_data1.to_excel('ematest2.xlsx',index = 'False') #excel export

# %%
###intraday minute data looper 1 MONTH AND SUBSEQUENT PLOTTING ALSO ON THE SAME LINES AS HISTORICAL DATA

dhan1=dhanhq(client_code,token_id)
securityId="13"
exchangeSegment="IDX_I"
instrument="INDEX"
expiryCode= 0
interval=5

i = date(2024,11,22)
today=date.today()
hist_intraday = pd.DataFrame()

#loop for weekly intraday 5 min data
while i < today:
    p=i-timedelta(days=4)
    fromDate=p.strftime('%Y-%m-%d')
    toDate = i.strftime('%Y-%m-%d')
    hist_data=dhan1.intraday_minute_data(securityId,exchangeSegment,instrument,fromDate,toDate,interval)
    hist_data1=pd.DataFrame(hist_data['data'])
    hist_data1['DATET'] = pd.to_datetime(hist_data1['timestamp'],unit = 's',utc=True).dt.tz_convert('Asia/Kolkata')
    hist_data1['DATET'] = pd.to_datetime(hist_data1['DATET'])
    hist_intraday=pd.concat([hist_intraday,hist_data1],ignore_index='True')
    print(i)
    i=i+timedelta(days=7)


print(hist_intraday) ##final output

# hist_intraday['DATET'] = hist_intraday['DATET'].dt.tz_localize(None)
# hist_intraday.to_excel('intraday5_Onemonth.xlsx',index = 'False')  ##excel export

##plot section

hist_data1 = hist_intraday
hist_data1['EMA20'] = talib.EMA(hist_data1['close'], timeperiod=20)
# hist_data1['EMA50'] = talib.EMA(hist_data1['close'], timeperiod=50)
hist_data1['EMA200'] = talib.EMA(hist_data1['close'], timeperiod=200)
# hist_data1["EMA200PD"] = hist_data1.close.ewm(span=200,adjust=False,min_periods=200).mean()
hist_data1["RSI14"] = talib.RSI(hist_data1['close'],timeperiod = 14)

# print(hist_data1[['EMA200PD','EMA200','RSI14']])
hist_data1.set_index('DATET', inplace=True)


ema_plot = mpf.make_addplot(hist_data1['EMA20'])
rsi_plot = mpf.make_addplot(hist_data1['RSI14'],panel=1, color='green', title='RSI 14')
mpf.plot(hist_data1, type='candle', style='charles', title="Candlestick Chart", ylabel='Price',addplot=[mpf.make_addplot(hist_data1[['EMA200','EMA20']]),rsi_plot],figsize=(10, 8), panel_ratios=(4,1))

# %%
##ticker data test

# # i=1
# while i in range(1):
#     i=i+1
#     ticker_input = {"IDX_I":[13]}
#     tick_data = dhan1.ticker_data(ticker_input)
#     print(tick_data)
#     time.sleep(1)

# # ticker_input = {"IDX_I":[13]}
# # quote_data = dhan1.quote_data(ticker_input)
# # quote_df = pd.DataFrame(quote_data['data']['data']['IDX_I']['13'])
# # print(quote_df)