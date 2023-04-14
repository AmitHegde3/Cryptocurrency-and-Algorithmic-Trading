import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import datetime
from pycoingecko import CoinGeckoAPI
from mplfinance.original_flavor import candlestick2_ohlc

dict_ = {'a':[11,21,31],'b':[12,22,32]}

df = pd.DataFrame(dict_)

print(type(df))

print(df.head())

print(df.mean())

cg = CoinGeckoAPI()

bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin',vs_currency='usd',days=30)
#print(bitcoin_data)
btc_price_data = bitcoin_data['prices']
#print(btc_price_data)
btc_price_data[0:5]
#print(btc_price_data)

data = pd.DataFrame(btc_price_data,columns = ['Timestamp','Price'])

#print(data)

data['date'] = data['Timestamp'].apply(lambda d:datetime.date.fromtimestamp(d/1000.0))

#print(data)

candlestick_data = data.groupby(data.date, as_index = False).agg({"Price":['min','max','first','last']})

#print(cs_data)

fig = go.Figure(data=[go.Candlestick(x=candlestick_data['date'],
                open=candlestick_data['Price']['first'], 
                high=candlestick_data['Price']['max'],
                low=candlestick_data['Price']['min'], 
                close=candlestick_data['Price']['last'])
                ])

fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()

