import pandas as pd
import numpy as np
import creds
import time
from finta import TA
import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.instruments as instruments
import tweepy as tweepy
import eur_usd
import usd_cad
import gbp_usd
import aud_usd
import eur_gbp
import usd_jpy


## Calls modules which contains subsequent fx pair data/trade action
eurusd = eur_usd.trade_eurusd()
usdcad = usd_cad.trade_usdcad()
gbpusd = gbp_usd.trade_gbpusd()
audusd = aud_usd.trade_audusd()
eurgbp = eur_gbp.trade_eurgbp()
usdjpy = usd_jpy.trade_usdjpy()

## Grabs the last 10 candle data for each DF
eurusd_last10 = eurusd.tail(10)
usdcad_last10 = usdcad.tail(10)
gbpusd_last10 = gbpusd.tail(10)
audusd_last10 = audusd.tail(10)
eurgbp_last10 = eurgbp.tail(10)
usdjpy_last10 = usdjpy.tail(10)

## Concatenates dataframes into 1 for better horizontal reading
horizontal_stack = pd.concat([eurusd_last10, usdcad_last10, gbpusd_last10, audusd_last10, eurgbp_last10, usdjpy_last10], axis = 1)

while True:
    print(horizontal_stack)
    time.sleep(60)
