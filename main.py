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


## Prints trade dataframe(s) for user to interpret
eur_usd.trade_eurusd()
usd_cad.trade_usdcad()
