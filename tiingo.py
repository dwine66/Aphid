# -*- coding: utf-8 -*-
"""
Created on Sun Aug 26 18:50:56 2018

@author: Dave
"""

# From https://api.tiingo.com/docs/tiingo/daily
# Example with ticker: GOOGL


"""
*************************
This is our favorite method
*************************
"""
#pd.read_json("https://api.tiingo.com/tiingo/daily/googl/prices?startDate=2012-1-1&endDate=2016-1-1&token=c217b3b6ce25e27828fdd6430d0d01ea94ae0487")


from datetime import datetime
import pandas as pd
import requests
import json

Ticker_Name = input('Stock Ticker Name: ')
print ('Retrieving data for',Ticker_Name)
SD_Stamp = '1980-01-01'
Date_Now = datetime.now()
ED_Stamp = str(Date_Now.year)+'-'+str(Date_Now.month)+'-'+str(Date_Now.day)
print (SD_Stamp,'to',ED_Stamp)
    
headers = {
'Content-Type': 'application/json',
'Authorization' : 'Token c217b3b6ce25e27828fdd6430d0d01ea94ae0487'
}
#requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/spy/prices?startDate=2012-1-1&endDate=2016-1-1",headers=headers)

# This works OK - returns last valid date even if date given is not a market day
requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/"+Ticker_Name+"/prices?startDate="+SD_Stamp+"&endDate="+ED_Stamp,headers=headers)

# Converts to a list of dictionaries
Ticker_Data = json.loads(requestResponse.text)
print (Ticker_Data[0])

# Then convert to dataframe
Ticker_DF = pd.DataFrame(Ticker_Data)

Ticker_DF['date'] = Ticker_DF['date'].str.slice(0,10)

# Then rearrange dataframe
T_DF_format = Ticker_DF.drop(['adjHigh','adjLow','adjOpen','adjVolume','divCash','splitFactor'],axis=1)
T_DF_ordered = T_DF_format[['date','adjClose','close','high','low','open','volume']]
if Ticker_Name == 'SPY':
    T_DF_ordered = T_DF_format[['date','open','high','low','close','adjClose','volume']]
    
T_DF_ordered.rename(index=str,columns={"date":"Date","adjClose":"Adj Close","close":"Close","high":"High","low":"Low","open":"Open","volume":"Volume"},inplace=True)
T_DF_ordered.set_index('Date',inplace=True)
T_DF_ordered.sort_index(axis=0,ascending=False,inplace=True)

T_DF_ordered.to_csv('S:\\Dave\\QH\\Aphid\\Static Data\\Yahoo_PH\\'+Ticker_Name+' Price History.csv')