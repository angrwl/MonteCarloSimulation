

'''========================================================== Monte Carlo simulations Demo =========================================================='''

import pandas as pd  #help you to perform functions on dictionaries 
import pandas_datareader.data as web #useful to get financial data from the web 
import numpy as np  
import datetime as dt
import matplotlib.pyplot as plt

start = dt.datetime(2018,6,29)
end = dt.datetime(2018,12,29)

''' 'APPL' is the stock price
     yahoo is the source
     start and end are the time
     since this is store as a dictionary, to call only the close price, we need to type the following'''


stock = 'AAPL'  #stock name
#data = web.DataReader(stock,'yahoo',start,end)
prices = web.DataReader(stock,'yahoo',start,end)['Close']

#returns = prices.pct_change()
# this is a inbuilt function in pandas to calculate returns
# but it can be done manually as shown below - here shift() takes the next value along in a dict

returns = (prices - prices.shift(1))/prices.shift(1)
returns = returns.shift(-1)  # this is so that we ignore the nan term at the start

last_price = prices[-1];

# no. of simulations
noOfSims = 1000;
noOfDays = 252;  #no. of working days in a year

simsDf = pd.DataFrame()  #will contain 1000 sims of daily prices of future (i.e. 252 values each sim)
# I could have also defined simsDf as {}, but pd.DataFrame represents data better - it is also a dict
vol = returns.std() #calculates volatility of the returns in the time frame given

for i in range(noOfSims):
    # we want to predict the future prices using the past
    priceSeries = [];
    #we assume returns are normally dist with mean = 0 and sd = daily vol
    startPrice = last_price*(1+np.random.normal(0,vol)); #here we mean startprice of the sims of future
    priceSeries.append(startPrice);
    for j in range(noOfDays-1):  #we only want 252 values and since we have initially appended a value, we have to subtract 1
        newPrice = priceSeries[j]*((1+np.random.normal(0,vol)));
        priceSeries.append(newPrice);

    simsDf[i] = priceSeries;


# plotting
# plt.style.use('dark_background')  #styling to make your plots have a dark backgroung (another one is ggplot)
plt.style.use('ggplot')
plt.figure()
plt.plot(simsDf);
plt.axhline(y = last_price,color = 'blue',linestyle = '-',linewidth = 3) #last price
plt.xlabel('Number of Days');
plt.ylabel('Predicted Prices');
plt.title('Monte Carlo: {}'.format(stock));
# ax = plt.gca()  #making the background black
# ax.set_facecolor('black')
plt.show()
