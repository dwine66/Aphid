# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 05:09:44 2019

Time Series Testing for stocks



@author: Dave
"""
### Libraries
import csv
import numpy as np
import pandas as pd
import os
import re
import math
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from datetime import datetime, timedelta
import dateutil

### Functions
def readcsv(fname):
    vname = pd.DataFrame(pd.read_csv(fname,na_values='n/a'))
    return vname

### Constants

### Main Code
WKdir='S:\\Dave\\QH\\Aphid\\Static Data\\Yahoo_PH'
os.chdir(WKdir)

# Read in sump pump data
filename='TNP Price History.csv'
print (filename)
Ticker_df = readcsv(filename)

#pd.to_numeric(Sump_df['Milone_Level_(cm)'])

# Make this a pandas time series
pd.to_datetime(Ticker_df['Date'])
# https://stackoverflow.com/questions/27032052/how-do-i-properly-set-the-datetimeindex-for-a-pandas-datetime-object-in-a-datafr
Ticker_df.set_index(pd.DatetimeIndex(Ticker_df['Date']),inplace = True)

## Plotting
Ticker_df['Close'].plot()

Ticker_df.ix['2016'].plot()

Ticker_df.resample('M',how='mean')
Ticker_df[datetime(2016,12,24):]

#fig=plt.figure('test',figsize=(9,3))
#plt.plot(Ticker_df['Close'],'r.')
#plt.show