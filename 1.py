# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 15:10:50 2021

@author: abdou
"""

# trading and tracking one coin

import pandas as pd
import math
from datetime import datetime
import ccxt ,json
from ccxt import binance

import csv
import talib
import urllib
from talib import *
from time import time, sleep
from contextlib import contextmanager
import requests
import warnings
import keys 
import keys2

warnings.filterwarnings('ignore')


def buycond(dx,indicators):
    n=0

    if indicators['macdhist'].iloc[-3]<indicators['macdhist'].iloc[-4] and indicators['macdhist'].iloc[-3]<indicators['macdhist'].iloc[-2] :
       if indicators['macdhist'].iloc[-2]<indicators['macdhist'].iloc[-1]:
           n=1
        
    return n




def sellcond(dx,indicators):
    m=0

    if indicators['macdhist'].iloc[-3]>indicators['macdhist'].iloc[-4] and indicators['macdhist'].iloc[-3]>indicators['macdhist'].iloc[-2] :
       if (indicators['macdhist'].iloc[-2]>indicators['macdhist'].iloc[-1]):
           m=1       
    return m

def sellcond2(dx,indicators):
    m=0
    if (indicators['macdhist'].iloc[-2]>indicators['macdhist'].iloc[-1]) : #or ((indicators['macdhist'].iloc[-2]>indicators['macdhist'].iloc[-1]) and indicators['macdhist'].iloc[-1]<0 ):
           m=1       
    return m

def sellcond3(dx,indicators):  
    m=0
    if (indicators['macdhist'].iloc[-3]>=indicators['macdhist'].iloc[-2]>indicators['macdhist'].iloc[-1]) : #or ((indicators['macdhist'].iloc[-2]>indicators['macdhist'].iloc[-1]) and indicators['macdhist'].iloc[-1]<0 ):
           m=1
    return m

lstp1=pd.DataFrame()
lstp2=pd.DataFrame()
lstp11=pd.DataFrame()
lstp22=pd.DataFrame()

hi=pd.DataFrame([])
aa=pd.DataFrame([])


def getdata(api,coin,frame,candles):
     exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
     })
     TA=pd.DataFrame()
     macdperiode=9
     market=exchange.load_markets()
     bars=exchange.fetch_ohlcv(coin,frame,limit=candles)
     df = pd.DataFrame(bars, columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
     df['Time']=[datetime.fromtimestamp(float(time)/1000) for time in df['Time']]
     macd, macdsignal, macdhist = talib.MACD(df['Close'], signalperiod=macdperiode)

     TA['macd']=macd
     TA['macdsignal']=macdsignal
     TA['macdhist']=macdhist
     del exchange
     return df,TA
 
def ordre(api,api2,coin):
    
                  exchange=ccxt.binance({
                      'apiKey':api.apiKey,
                      'secret':api.secretKey
    
                  })
                  exchange2=ccxt.binance({
                       'apiKey':api2.apiKey,
                       'secret':api2.secretKey
    
                  })
                  balance=exchange.fetch_balance()
                  
                  ss=coin.split('/')
                  ss=ss[0]
                  amount=balance[ss]['free'] 
                  sellordre=exchange.createMarketSellOrder (coin, amount)
                  
                  balance2=exchange2.fetch_balance()
                  amount2=balance2[ss]['free']
                  #sellordre2=exchange2.createMarketSellOrder (coin, amount2)
                  print('coin was selled')
                  del exchange
                  del exchange2
                  return sellordre
                  
                  
def getcoin():
    a= pd.read_csv('backtesting results.csv',index_col=0)     
    a=a[a['number of losses']==0]
    a = a.sort_values(by=['number of gains'])
    sym=a.index[-1]
    
    return sym
    
    
def loopforbuy(api,api2,n):    
    buy=0
    x=0
    exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
    })
    exchange2=ccxt.binance({
               'apiKey':api2.apiKey,
               'secret':api2.secretKey
    
    })
    n=0
    while n==0:
        
        pp=0
        df,TA=getdata(api,symbol,frame,limit)
        n=buycond(df,TA)
        print('waiting for buying')
        if n==1:
            sleep(60)
            df,TA=getdata(api,symbol,frame,limit)
            n=buycond(df, TA) 
        if n==1:
            
            lastprice=exchange.fetch_ticker(symbol)
            lastp=float(lastprice['last'])
            ordre=exchange.create_market_buy_order(symbol, howmuch/lastp)
            #ordre2=exchange2.create_market_buy_order(symbol, howmuch2/lastp)
            print('buying condition is on, i buyed the coin')
            buy=1
            x=ordre['info']['fills'][0]['price']
        sleep(150)
        
          
    del exchange    
    return buy,x



def loopforsell(api,api2,bb,x):
    x=float(x)    
    sell=0
    exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
    })
    exchange2=ccxt.binance({
                       'apiKey':api2.apiKey,
                       'secret':api2.secretKey
    
    })
    k=0
    while sell==0:
       k=0
       sell=0
       df,TA=getdata(api,symbol,frame,limit)
       m=sellcond(df,TA)
       ss=symbol.split('/')
       ss=ss[0]  
       balance=exchange.fetch_balance()
                  

       amount=balance[ss]['free']
       
                  
       balance2=exchange2.fetch_balance()
       amount2=balance2[ss]['free'] 
       
       print('waiting to sell')
       lastprice=exchange.fetch_ticker(symbol)
       lastp=float(lastprice['last'])
       oss=x*amount
       oss2=x*amount2
       if m==1 and sell==0:
           k=0
           print('second chance before selling')
           sleep(150)
           df,TA=getdata(api,symbol,frame,limit)
           k=sellcond3(df,TA)
           if k==1:
               sellordre=ordre(api,api2,symbol)
               so=sellordre['info']['fills'][0]['price']
               print('coin has been selled')
               sell=1       
       ss=symbol.split('/')
       ss=ss[0]           
           
       balance=exchange.fetch_balance()
                  

       amount=balance[ss]['free']
       
                  
       balance2=exchange2.fetch_balance()
       amount2=balance2[ss]['free'] 
       
       print('waiting to sell')
       lastprice=exchange.fetch_ticker(symbol)
       lastp=float(lastprice['last'])
       oss=x*amount
       oss2=x*amount2
       
       
       if lastp<=0.983*x and sell==0:
           sellordre=ordre(api,api2,symbol)
           so=sellordre['info']['fills'][0]['price']
           print('coin has been selled')
           sell=1
       """if lastp>=1.01*x and oss>5 and oss2>5:
           sellordre=ordre(api,api2,symbol)
           so=sellordre['info']['fills'][0]['price']
           print('coin has been selled')
           sell=1"""
       balance=exchange.fetch_balance()
                  

       amount=balance[ss]['free']
       
                  
       balance2=exchange2.fetch_balance()
       amount2=balance2[ss]['free']   
       oss=x*amount
       oss2=x*amount2

       if k==1 and sell==0:
           sellordre=ordre(api,api2,symbol)
           so=sellordre['info']['fills'][0]['price']
           print('coin has been selled')
           sell=1

       
       sleep(150) 
       
       balance=exchange.fetch_balance()
                  

       amount=balance[ss]['free']
       
                  
       balance2=exchange2.fetch_balance()
       amount2=balance2[ss]['free'] 
       lastprice1=exchange.fetch_ticker(symbol)
       lastp1=float(lastprice1['last'])
       oss=x*amount
       oss2=x*amount2
       df,TA=getdata(api,symbol,frame,limit)
       lmn=sellcond3(df,TA)
       if lmn==1 and sell==0:
           sellordre=ordre(api,api2,symbol)
           so=sellordre['info']['fills'][0]['price']
           print('coin has been selled')
           sell=1           
       balance=exchange.fetch_balance()
                  

       amount=balance[ss]['free']
       
                  
       balance2=exchange2.fetch_balance()
       amount2=balance2[ss]['free'] 
       lastprice1=exchange.fetch_ticker(symbol)
       lastp1=float(lastprice1['last'])
       oss=x*amount
       oss2=x*amount2
       if lastp1<=0.983*x and sell==0:
           sellordre=ordre(api,api2,symbol)
           so=sellordre['info']['fills'][0]['price']
           print('coin has been selled')
           sell=1
       """if lastp1>=1.04*x and oss>5 and oss2>5:
           sellordre=ordre(api,api2,symbol)
           so=sellordre['info']['fills'][0]['price']
           print('coin has been selled')
           sell=1"""
    del exchange
    return k,so

limit=55
howmuch=20
howmuch2=20
frame='5m'



def main(p,q):
    n,x=loopforbuy(keys2,keys,p)
    #nn,xx=loopforbuy(keys,p)
    print(x)
    l,so=loopforsell(keys2,keys,n,x)
    #ll,so=loopforsell(keys,nn,xx)
    print('round number   ',q ,'  finished')
    return x,float(so)
q=0

while True:
    try:
       symbol=getcoin()
       df,TA=getdata(keys2,symbol,frame,limit)
       n1=buycond(df,TA)
       x,so=main(n1,q)
       lst=pd.DataFrame([[x,so]],columns=['buyed at','selled at'])
       lstp11=lstp11.append(lst)
       lstp11.to_csv('btc trading history.csv')
       print(lstp11)
       q=q+1
    except:
         print('error')
         pass

    
        
    

    