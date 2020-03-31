import pandas as pd
import numpy as np
import creds
from finta import TA
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments

#Initializing credientials to the account
client = oandapyV20.API(access_token=creds.APIKEY)
accountID = creds.accID
account_summary = accounts.AccountSummary(accountID)
client.request(account_summary)
account_details = account_summary.response 


## Determines how much margin to allocate to each trade, and the max number of active trades, 5 active trades, 3% per trade
balance = account_details['account']['balance'] 
trade_size = float(balance) *.03 
max_open_trades = 5


## Gets candlestick data for the tickers specified for the timeframe specified 
params = {
    'count': 200,
    'granularity': 'M30'
}
eurusd = instruments.InstrumentsCandles(instrument="EUR_USD", params = params)
eurusd_candles = client.request(eurusd)


## Puts candle close time into a list
candle_times = []
candle_close_time = eurusd_candles['candles']
for i in candle_close_time:
    close_time = i['time']
    candle_times.append(close_time)


## Puts all candle values into lists
close_values = []
candle_data_close = eurusd_candles['candles']
for i in candle_data_close:    
    close_price = i['mid']['c']
    close_values.append(float(close_price))
##
open_values = []
candle_data_open = eurusd_candles['candles']
for i in candle_data_open:
    open_price = i['mid']['o']
    open_values.append(float(open_price))
##
high_values = []
candle_data_high = eurusd_candles['candles']
for i in candle_data_high:
    high_price = i['mid']['h']
    high_values.append(float(high_price))
## 
low_values = []
candle_data_low = eurusd_candles['candles']
for i in candle_data_low:
    low_price = i['mid']['l']
    low_values.append(float(low_price))
    

## Makes pandas dataframe , imports ohlc from last 300 candles
## Zip the 4 lists to create a list of tuples
zippedList = list(zip(open_values, high_values, low_values, close_values))
df = pd.DataFrame(zippedList, columns = ['open' , 'high', 'low', 'close'])



## %B Indicator, adds %b to dataframe
bb = TA.PERCENT_B(df)
df["%BB"] = bb

## Adds time to df
df['Time'] = candle_times


## Replaces NaN values with 0.0 so index length is the same for trade_signal, and bb columns
bb = np.nan_to_num(bb)

## Determines action to take based on %b value , ads trade column to dataframe
trade_signal = []
for i in bb:
    
    if i == 0:
        trade_signal.append('N'),
    elif i > 1:
        trade_signal.append('Sell'),
    elif i < 0:
        trade_signal.append('Buy'),
    elif i <= 1 and i >= 0:
        trade_signal.append('N')
print(len(bb))
print(len(trade_signal))

action = pd.DataFrame(trade_signal)
df['Trade'] = action


pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
print(df)
