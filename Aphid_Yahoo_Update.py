# -*- coding: utf-8 -*-
"""
Created on 9/15/2017

Aphid_Yahoo_Update

This module opens the existing SPY file in Price History, gets data from Yahoo
for any missing dates after the latest entry up to the current date, then
re-saves the csv file.  It does not alter any excel files.

Revision History
Rev 0.1: 9/15/2017: Built from Aphid_SPY_Update - Works OK!
Rev 0.2: 9/24/2017: Moved Tname data pull under try loop.
@author: Dave
"""

### Libraries
#import openpyxl as op
import os
import pandas as pd
import pandas_datareader as pdr
import fix_yahoo_finance as yf
import itertools
import openpyxl as op
from datetime import datetime, timedelta

yf.pdr_override()
### Functions
def GetTickerData(Tname,filename):
    # Read in existing CSV
    print (Tname)
    Tname_csv = pd.read_csv(filename)
    # Sort by reverse date
    Date_ts = pd.to_datetime(Tname_csv['Date'],infer_datetime_format=True)
    Tname_csv = Tname_csv.drop(['Date'],axis=1)
    Tname_csv = pd.concat([Date_ts,Tname_csv],axis=1)
    Tname_csv.set_index(['Date'],inplace=True)
    
    ## Get current date
    date_now = datetime.now()-timedelta(days=2)
    print ('Currrent Date:',date_now)
    print ('Current Weekday:', date_now.weekday)
    #Fix this so the stock ticker uses the previous day's date if early in the morning
    
    #Fix weekends - go back and grab Friday
    if date_now.weekday == 6: #Saturday
        print ('Saturday')
        date_now=date_now-timedelta(days=1)
    elif date_now.weekday == 0: #Sunday
        print ('Sunday')
        date_now=date_now-timedelta(days=2)
    #Try to fix this to recursively go back if it fails
    date_last = Tname_csv.index[0]# Get most recent date from existing CSV file
    # convert object to the format we want
    formatted_date = date_now.strftime('%Y-%m-%d')
    print ('Current Formatted Date:',formatted_date)
    # Tname is an ETF that tracks the SP500 with data back to 1994.
    # Multiply by 10 to get index value
    # But volume data is different from volume of SP500
    
    try:
        Tname_yahoo = pdr.get_data_yahoo(Tname, date_last,date_now)[1:]
        print('Yahoo Date Request',Tname_yahoo)
    ## Add more test logic here
    
        # Open Aphid Data Feeds and write latest Tname data
        Tname_new = pd.concat([Tname_csv,Tname_yahoo])
        Tname_new = Tname_new.sort_index(ascending=False)
        # Maybe some code here to check column order        
        if filename[0:3] != 'SPY':    
            Tname_new = Tname_new[['Date','Adj Close','Close','High','Low','Open','Volume']]
        else:
            Tname_new = Tname_new[['Date','Open','High','Low','Close','Adj Close','Volume']]
        # Write new file back
        Tname_new.to_csv(filename)
    except:
        print ('Data not available for',date_now)
        
def GetTickerName():
    input_name = input('Ticker: ')   
    return input_name

### Main Code

## Setup

# WKdir = 'C:\\Users\\Dave\\Desktop\\'
WKdir= 'S:\\Dave\\QH\\Aphid\\Static Data\\Yahoo_PH\\'
os.chdir(WKdir)
fnameroot = ' Price History.csv'

#Need T/E loop here
ticker_name = GetTickerName()
try:
    len(ticker_name)>4
    ## Add more test logic here
except:
    print ('invalid ticker symbol')
    GetTickerName

filename = ticker_name + fnameroot
print ('Getting Ticker Data for ',ticker_name)
GetTickerData(ticker_name, filename)
print (ticker_name,'data updated')

filename = 'SPY' + fnameroot
print ('Getting Ticker Data for SPY')
GetTickerData('SPY',filename)
print ('SPY data updated')



