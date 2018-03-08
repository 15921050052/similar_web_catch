# -*- coding: utf-8 -*-
import requests
# https://api.hitbtc.com/api/2/public/trades/ETHBTC
url = "https://poloniex.com/public?command=returnTradeHistory&start=1520294400&end=1520295050&currencyPair=BTC_NXT"

response = requests.request("GET", url)

print(response.text)
