### LINK TO HOW-TO : https://oanda-api-v20.readthedocs.io/en/latest/oanda-api-v20.html

### %B = [(Price – Lower Band) / (Upper Band – Lower Band)] * 100

##   * Middle Band = 20-day simple moving average (SMA)
##* Upper Band = 20-day SMA + (20-day standard deviation of price x 2) 
##* Lower Band = 20-day SMA - (20-day standard deviation of price x 2)
import pandas as pd
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
    'granularity': 'M5'
}
eurusd = instruments.InstrumentsCandles(instrument="EUR_USD", params = params)
eurusd_candles = client.request(eurusd)


## Puts all candle values into lists
close_values = []
candle_data_close = eurusd_candles['candles']
for i in candle_data_close:    
    close_price = i['mid']['c']
    close_values.append(close_price)
##
open_values = []
candle_data_open = eurusd_candles['candles']
for i in candle_data_open:
    open_price = i['mid']['o']
    open_values.append(open_price)
##
high_values = []
candle_data_high = eurusd_candles['candles']
for i in candle_data_high:
    high_price = i['mid']['h']
    high_values.append(high_price)
## 
low_values = []
candle_data_low = eurusd_candles['candles']
for i in candle_data_low:
    low_price = i['mid']['l']
    low_values.append(low_price)


## Makes pandas dataframe , imports ohlc from last 300 candles
# Zip the 4 lists to create a list of tuples
zippedList = list(zip(open_values, high_values, low_values, close_values))
df = pd.DataFrame(zippedList, columns = ['open' , 'high', 'low', 'close'])


## Determines trend 
uptrend = None
downtrend = None
trend = None

start_price = close_values[0]
end_price = close_values[199]

if start_price < end_price:
    uptrend = True
elif start_price > end_price:
    downtrend = True

if uptrend == True:
    downtrend = False
    trend = 'up'
elif downtrend == True:
    uptrend = False
    trend = 'down'



###

#If trend = up insert buy only code
#If trend = down insert sell only code

###


## %B Indicator
print(df)
bb = TA.PERCENT_B(df)
