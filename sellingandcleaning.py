"""
Created on Sat Jul 24 01:48:06 2021

@author: abdou
"""

import pandas as pd
import math
from datetime import datetime
import ccxt ,json
from ccxt import binance
import keys
import keys2
import talib
import requests
from talib import *

 
def gettingbalances(kys):
     exchange=ccxt.binance({
                      'apiKey':kys.apiKey,
                      'secret':kys.secretKey
    
     })

     balance=exchange.fetch_balance()
     
     balance=pd.DataFrame(balance['info']['balances'][:])
     balance=balance[(balance['free'].astype(float))>0]
     bb=balance
     a=balance['asset'].copy()+'/USDT'
     reshape=balance.copy()
     reshape['asset']=a
     
     return bb,reshape
 
  

def barr(exchange,coin,frame,candles):
     
     TA=pd.DataFrame()
     macdperiode=9
     market=exchange.load_markets()
     bars=exchange.fetch_ohlcv(coin,frame,limit=candles)
     df = pd.DataFrame(bars, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
     df['Time']=[datetime.fromtimestamp(float(time)/1000) for time in df['Time']]
     sy=pd.DataFrame()
     for i in range(len(df)):
         sy=sy.append([coin])
     sy=sy.reset_index(drop=True)
     #print(sy)
     df['symbol']=sy
     macd, macdsignal, macdhist = talib.MACD(df['Close'], signalperiod=macdperiode)
     TA['macd']=macd
     TA['macdsignal']=macdsignal
     TA['macdhist']=macdhist
   
     return df,TA

     
def sellingbot(kys):
     exchange=ccxt.binance({
                      'apiKey':kys.apiKey,
                      'secret':kys.secretKey
    
     })
     bl,bm=gettingbalances(kys)
     for s,x in zip(bm['asset'],bm['free'].astype(float)):
         if x>0:
             try:
                 sellordre=exchange.createMarketSellOrder (s, x)
                 print(sellordre['info']['fills'][0]['price'])
             except :
                 print('not valid amount')
                 pass
             
                
def watching(api):
     exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
     })
             
     dfbtc,tabtc=barr(exchange,'BTC/USDT','4h',45)
     
     if dfbtc['Close'].iloc[-1]<40000:
                  link0='https://api.telegram.org/bot1749382225:AAFm6D497qfMFkuwLTfUsCOPePGq9E1lvog/sendMessage?chat_id=-566915440&text= xxx BTC WARNING !!!!!!!'
                  link1='https://api.telegram.org/bot1749382225:AAFm6D497qfMFkuwLTfUsCOPePGq9E1lvog/sendMessage?chat_id=-566915440&text= xxx------"{}"-----xxx'.format('BTC/USDT')
                  requests.get(link0)
                  requests.get(link1)
                  low=dfbtc['Low'].iloc[-2]
                  close=dfbtc['Close'].iloc[-2]
                  symbol='BTC/USDT'
                  
                  link2='https://api.telegram.org/bot1749382225:AAFm6D497qfMFkuwLTfUsCOPePGq9E1lvog/sendMessage?chat_id=-566915440&text= BTC has closed under"{}"'.format(close)
                  link3='https://api.telegram.org/bot1749382225:AAFm6D497qfMFkuwLTfUsCOPePGq9E1lvog/sendMessage?chat_id=-566915440&text= BTC low of the candle "{}"'.format(low)
                  requests.get(link2)
                  requests.get(link3)
          

def getcoin():
    a= pd.read_csv('backtesting results.csv',index_col=0)     
    a=a[a['number of losses']==0]
    a = a.sort_values(by=['number of gains'])
    sym=a.tail(6)
    sym=sym.index
    coins=pd.DataFrame(sym)
    coins=coins.T
    return coins

