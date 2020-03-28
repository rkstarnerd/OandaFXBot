### LINK TO HOW-TO : https://oanda-api-v20.readthedocs.io/en/latest/oanda-api-v20.html

import creds
import time
import oandapyV20
import oandapyV20.endpoints.accounts as accounts

client = oandapyV20.API(access_token=creds.APIKEY)
accountID = creds.accID

r = accounts.AccountSummary(accountID)

client.request(r)
account_details = r.response #Object containing account summary 

balance = account_details['account']['balance'] # Account balance
trade_size = float(balance) *.05 #Margin allocated to each trade




