# -*- coding: utf-8 -*-
"""
Created on 9/6/2017

Aphid_SPY_Update

This module opens the existing SPY file in Price History, gets data from Yahoo
for any missing dates after the latest entry up to the current date, then
re-saves the csv file.  It does not alter any excel files.

Revision History
Rev 0.1: 9/6/2017:  Initial Work
Rev 0.2: 9/14/2017: First working version - works OK from LAIR and with Aphid_B
@author: Dave
"""

### Libraries
#import openpyxl as op
import os
import pandas as pd
import pandas_datareader as pdr
import itertools
import openpyxl as op
from datetime import datetime, timedelta

### Main Code

# Setup
# WKdir = 'C:\\Users\\Dave\\Desktop\\'
WKdir= 'Z:\\Dave\\QH\\Aphid\\Static Data\\Yahoo_PH\\'
os.chdir(WKdir)
filename='SPY Price History.csv'

# Read in existing CSV
SPY_csv = pd.read_csv(filename)
# Sort by reverse date
Date_ts = pd.to_datetime(SPY_csv['Date'],infer_datetime_format=True)
SPY_csv = SPY_csv.drop(['Date'],axis=1)
SPY_csv = pd.concat([Date_ts,SPY_csv],axis=1)
SPY_csv.set_index(['Date'],inplace=True)

## Get current date
date_now = datetime.now()
date_last = SPY_csv.index[0]# Get most recent date from existing CSV file
date_delta = date_now-date_last
# convert object to the format we want
formatted_date = date_now.strftime('%Y-%m-%d')
print (formatted_date)
# SPY is an ETF that tracks the SP500 with data back to 1994.
# Multiply by 10 to get index value
# But volume data is different from volume of SP500
# Put this in a try/except loop

#for i in range(0,date_delta.days):
#date_request = date_last + timedelta
#print (date_request,'\n')
try:
    SPY_yahoo = pdr.get_data_yahoo('SPY', date_last,date_now)[1:]
    print(SPY_yahoo)
except:
    print ('Data not available for',date_now)
    
# Open Aphid Data Feeds and write latest SPY data
SPY_new = pd.concat([SPY_csv,SPY_yahoo])
SPY_new = SPY_new.sort_index(ascending=False)

SPY_new.to_csv(filename)
'''
### Scraps
SP500_table = pd.DataFrame()
# Open Aphid Data Feeds and pull in existing table
wb=op.load_workbook('Aphid_DF_test.xlsx')
sheets = wb.get_sheet_names()
sheet_SP500 = wb.get_sheet_by_name('qry_SP500')
last_row = sheet_SP500.max_row

# from https://openpyxl.readthedocs.io/en/default/pandas.html
data = sheet_SP500.values
cols = next(data)[1:]
data = list(data)
idx = [r[0] for r in data]
data = (itertools.islice(r, 1, None) for r in data)
df = pd.DataFrame(data, index=idx, columns=cols)
'''