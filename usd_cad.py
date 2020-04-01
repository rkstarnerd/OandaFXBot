import pandas as pd
import numpy as np
import creds
import time
from finta import TA
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import tweepy as tweepy


def trade_usdcad():


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
        'count': 100,
        'granularity': 'M15'
    }
    usdcad = instruments.InstrumentsCandles(instrument="USD_CAD", params = params)
    usdcad_candles = client.request(usdcad)


    ## Puts candle close time into a list
    candle_times = []
    candle_close_time = usdcad_candles['candles']
    for i in candle_close_time:
        close_time = i['time']
        candle_times.append(close_time)


    ## Puts all candle values into lists
    close_values = []
    candle_data_close = usdcad_candles['candles']
    for i in candle_data_close:    
        close_price = i['mid']['c']
        close_values.append(float(close_price))
    ##
    open_values = []
    candle_data_open = usdcad_candles['candles']
    for i in candle_data_open:
        open_price = i['mid']['o']
        open_values.append(float(open_price))
    ##
    high_values = []
    candle_data_high = usdcad_candles['candles']
    for i in candle_data_high:
        high_price = i['mid']['h']
        high_values.append(float(high_price))
    ## 
    low_values = []
    candle_data_low = usdcad_candles['candles']
    for i in candle_data_low:
        low_price = i['mid']['l']
        low_values.append(float(low_price))
        

    ## Makes pandas dataframe , imports ohlc from last 300 candles
    ## Zip the 4 lists to create a list of tuples
    zippedList = list(zip(open_values, high_values, low_values, close_values))
    df1 = pd.DataFrame(zippedList, columns = ['open' , 'high', 'low', 'close'])



    ## %B Indicator, adds %b to dataframe
    bb = TA.PERCENT_B(df1)
    df1["%BB"] = bb

    ## Adds time to df, formats all the extra zeros in the time data
    df1['Time'] = candle_times
    df1['USD/CAD'] = df1['Time'].map(lambda x: str(x)[:-11])


    ## Replaces NaN values with 0.0 so index length is the same for trade_signal, and bb columns
    bb = np.nan_to_num(bb)

    ## Determines action to take based on %b value , ads trade column to dataframe
    trade_signal = []
    for i in bb:
        
        if i == 0:
            trade_signal.append('_'),
        elif i > 1:
            trade_signal.append('Sell'),
        elif i < 0:
            trade_signal.append('Buy'),
        elif i <= 1 and i >= 0:
            trade_signal.append('_')

    action = pd.DataFrame(trade_signal)
    df1['Trade'] = action


    ## This code formats the pandas db for viewer ease of use
    pd.set_option('display.width', None)
    pd.set_option('display.max_rows', 10)


    ## This code makes connection to twitter and tweets buy/sell signals
    #auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
    #auth.set_access_token(creds.access_token, creds.access_token_secret)
    #api = tweepy.API(auth)

   
    ## Adds blank columns to seperate the trade pairs visually
    df1['----------'] = ""


    ## Prints dataframe for viewer to interpret
    print(df1[['USD/CAD', 'Trade', '----------']])
