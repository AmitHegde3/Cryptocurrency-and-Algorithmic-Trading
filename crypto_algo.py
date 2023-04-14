import yfinance as yf
import pandas as pd
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.dates import DateFormatter

BTC_USD = yf.download("BTC-USD",start='2020-01-01', end = '2022-12-31',interval='1d')

print(BTC_USD.head(20))


#---------------------Creating a plot-------------------------------
fig,ax = plt.subplots(dpi=200)

date_format = DateFormatter("%h-%d-%y")

ax.xaxis.set_major_formatter(date_format)
ax.tick_params(axis='x',labelsize=8)
fig.autofmt_xdate()

ax.plot(BTC_USD['Close'],lw=0.75)

ax.set_ylabel('Price of bitcoin(USD)')
ax.set_title("Bitcoin to USD Exchange Rate")
ax.grid()

#plt.show()

#--------------------Simple Moving average of 9 days-----------------

BTC_USD['SMA_9'] = BTC_USD['Close'].rolling(window=9,min_periods=1).mean() 
BTC_USD['SMA_30'] = BTC_USD['Close'].rolling(window=30,min_periods=1).mean() 

print(BTC_USD.tail())


#-------------------Plotting SMA--------------------------------------
fig, ax = plt.subplots(dpi=200)

# Formatting the date axis
date_format = DateFormatter("%h-%d-%y")
ax.xaxis.set_major_formatter(date_format)
ax.tick_params(axis='x', labelsize=8)
fig.autofmt_xdate()

# Plotting the closing price against the date (1 day interval)
ax.plot(BTC_USD['Close'], lw=0.75, label='Closing Price') # Added label


ax.plot(BTC_USD['SMA_9'], lw=0.75, alpha=0.75, label='9 Day SMA')
ax.plot(BTC_USD['SMA_30'], lw=0.75, alpha=0.75, label='30 Day SMA')


# Adding labels and title to the plot
ax.set_ylabel('Price of Bitcoin (USD)')
ax.set_title('Bitcoin to USD Exchange Rate')
ax.grid() # adding a grid
ax.legend() # adding a legend

# Displaying the price chart
plt.show()

trade_signals = pd.DataFrame(index = BTC_USD.index)

short_interval = 10
long_interval = 40

trade_signals['Short'] = BTC_USD['Close'].rolling(window=short_interval, min_periods=1).mean()
trade_signals['Long'] = BTC_USD['Close'].rolling(window=long_interval, min_periods=1).mean()


trade_signals['Signal'] = 0.0

trade_signals['Signal'] = np.where(trade_signals['Short'] > trade_signals['Long'], 1.0,0.0)

trade_signals['Position'] = trade_signals['Signal'].diff()


#-------------------------------Plotting-------------------------------------------

fig, ax = plt.subplots(dpi=200)

# Formatting the date axis
date_format = DateFormatter("%h-%d-%y")
ax.xaxis.set_major_formatter(date_format)
ax.tick_params(axis='x', labelsize=8)
fig.autofmt_xdate()


# Plotting the Bitcoin closing price against the date (1 day interval)
ax.plot(BTC_USD['Close'], lw=0.75, label='Closing Price')

# Plot the shorter-term moving average
ax.plot(trade_signals['Short'], lw=0.75, alpha=0.75, color='orange', label='Short-term SMA')

# Plot the longer-term moving average
ax.plot(trade_signals['Long'], lw=0.75, alpha=0.75, color='purple', label='Long-term SMA')


# Adding green arrows to indicate buy orders
ax.plot(trade_signals.loc[trade_signals['Position']==1.0].index, trade_signals.Short[trade_signals['Position'] == 1.0],
 marker=6, ms=4, linestyle='none', color='green')

 # Adding red arrows to indicate sell orders
ax.plot(trade_signals.loc[trade_signals['Position'] == -1.0].index, trade_signals.Short[trade_signals['Position'] == -1.0],
 marker=7, ms=4, linestyle='none', color='red')


# Adding labels and title to the plot
ax.set_ylabel('Price of Bitcoin (USD)')
ax.set_title('Bitcoin to USD Exchange Rate')
ax.grid() # adding a grid
ax.legend() # adding a legend

# Displaying the price chart
plt.show()


initial_balance = 10000

backtest = pd.DataFrame(index = trade_signals.index)

backtest["BTC_Return"] = BTC_USD['Close'] / BTC_USD['Close'].shift(1)

# Add column containing the daily percent returns of the Moving Average Crossover strategy
backtest['Alg_Return'] = np.where(trade_signals.Signal == 1, backtest.BTC_Return, 1.0)

# Add column containing the daily value of the portfolio using the Crossover strategy
backtest['Balance'] = initial_balance * backtest.Alg_Return.cumprod() # cumulative product


fig, ax = plt.subplots(dpi=200)

# Formatting the date axis
date_format = DateFormatter("%h-%d-%y")
ax.xaxis.set_major_formatter(date_format)
ax.tick_params(axis='x', labelsize=8)
fig.autofmt_xdate()

# Plotting the value of Buy and Hold Strategy
ax.plot(initial_balance*backtest.BTC_Return.cumprod(), lw=0.75, alpha=0.75, label='Buy and Hold')

# Plotting total value of Crossing Averages Strategy
ax.plot(backtest['Balance'], lw=0.75, alpha=0.75, label='Crossing Averages')

# Adding labels and title to the plot
ax.set_ylabel('USD')
ax.set_title('Value of Portfolio')
ax.grid() # adding a grid
ax.legend() # adding a legend

# Displaying the price chart
plt.show()

