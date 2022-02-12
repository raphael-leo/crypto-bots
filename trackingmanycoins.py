# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 11:59:55 2021

@author: abdou
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 15:10:50 2021

@author: abdou
"""

# trading and tracking many coins
import sellingandcleaning
from sellingandcleaning import *
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

    if indicators['macdhist'].iloc[-3]<indicators['macdhist'].iloc[-4] and indicators['macdhist'].iloc[-3]<indicators['macdhist'].iloc[-2] and indicators['macdhist'].iloc[-3]<=0:
       if indicators['macdhist'].iloc[-2]<indicators['macdhist'].iloc[-1]:
           n=1
        
    return n
def buycondbtc(dx,tax):
    nbtc=0
    if tax['macdhist'].iloc[-3]<tax['macdhist'].iloc[-2]  and tax['macdhist'].iloc[-2]<tax['macdhist'].iloc[-1]:
        nbtc=1
    return nbtc

def loopforbuy(api,n):    
    buy=pd.DataFrame([0,0,0,0,0])
    x=0
    exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
    })
    while n==0:
        pp=0
        df,TA=getdata(api,symbol,frame,limit)
        n=buycond(df,TA)
        print('waiting for buying')
        if n==1:
            
            lastprice=exchange.fetch_ticker(symbol)
            lastp=float(lastprice['last'])
            ordre=exchange.create_market_buy_order(symbol, howmuch/lastp)
            print('buying condition is on, i buyed the coin')
            buy=1
            x=ordre['info']['fills'][0]['price']
        sleep(20)
        
          
    del exchange    
    return buy,x







def sellcond(dx,indicators):
    mm=0

    if indicators['macdhist'].iloc[-3]>indicators['macdhist'].iloc[-4] and indicators['macdhist'].iloc[-3]>indicators['macdhist'].iloc[-2] :
          mm=1
        
    return mm

def sellcond3(dx,indicators):  
    m=0
    if (indicators['macdhist'].iloc[-3]>=indicators['macdhist'].iloc[-2] and indicators['macdhist'].iloc[-2]>indicators['macdhist'].iloc[-1]) : #or ((indicators['macdhist'].iloc[-2]>indicators['macdhist'].iloc[-1]) and indicators['macdhist'].iloc[-1]<0 ):
           m=1
    return m

def sellcondbtc(dx,tax):
    mbtc=0
    if tax['macdhist'].iloc[-3]>tax['macdhist'].iloc[-2]  and tax['macdhist'].iloc[-2]>tax['macdhist'].iloc[-1]:
        mbtc=1
    return mbtc


lstp1=pd.DataFrame()
lstp2=pd.DataFrame()
lstp11=pd.DataFrame()
lstp22=pd.DataFrame()

hi=pd.DataFrame([])
aa=pd.DataFrame([])

                

    
def getcoin():
    a= pd.read_csv('backtesting results.csv',index_col=0)     
    a=a[a['number of losses']==0]
    a = a.sort_values(by=['number of gains'])
    sym=a.tail(6)
    sym=sym.index
    coins=pd.DataFrame(sym)
    coins=coins.T
    return coins




coins=getcoin()





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






def getdata(api,frame,limit):
     
     global coins
     exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
     })
     a=limit
     df = pd.DataFrame()
     TA = pd.DataFrame()
     
     df0,TA0=barr(exchange,coins[0][0],frame,a)
     df1,TA1=barr(exchange,coins[1][0],frame,a)
     df2,TA2=barr(exchange,coins[2][0],frame,a)
     df3,TA3=barr(exchange,coins[3][0],frame,a)
     df4,TA4=barr(exchange,coins[4][0],frame,a)
     df5,TA5=barr(exchange,coins[5][0],frame,a)
     

     #df=pd.DataFrame([[df0,df1,df2,df3,df4]],columns=[coins[0][0],coins[1][0],coins[2][0],coins[3][0],coins[4][0]])
     #TA=pd.DataFrame([[TA0,TA1,TA2,TA3,TA4]],columns=[coins[0][0],coins[1][0],coins[2][0],coins[3][0],coins[4][0]])
    
     return df0,df1,df2,df3,df4,df5,TA0,TA1,TA2,TA3,TA4,TA5
 
def balance(api):
    exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
     })
    balance=exchange.fetch_balance()
    bk=balance.copy()
    balance=pd.DataFrame(balance['info']['balances'][:])
    balance=balance[(balance['free'].astype(float))>0]
    a=balance['asset']+'/USDT'
    reshape=balance
    reshape['asset']=a
    
    return reshape,balance,bk

def getcoinbalance(api,coin):
    bs,ba,k=balance(api)
    cn=coin
    cn=cn.split('/')
    cn=cn[0]
    bcoin=float(k[cn]['free'])
    return bcoin

def getallcoinsbalance(api,syms):
    b0=getcoinbalance(api,syms[0].iloc[0])
    b1=getcoinbalance(api,syms[1].iloc[0])
    b2=getcoinbalance(api,syms[2].iloc[0])
    b3=getcoinbalance(api,syms[3].iloc[0])
    b4=getcoinbalance(api,syms[4].iloc[0])
    b5=getcoinbalance(api,syms[5].iloc[0])
    usdt=getcoinbalance(api,'USDT')
    return b0,b1,b2,b3,b4,b5,usdt




        
    
def usdtbl(api):
    usdt=getcoinbalance(api,'USDT')
    return usdt
    

def lastprices(api):
    exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
     })
    
    df0,df1,df2,df3,df4,df5,TA0,TA1,TA2,TA3,TA4,TA5=getdata(api,'5m',55)
    
    lastprice0=exchange.fetch_ticker(df0['symbol'][0])
    lastp0=float(lastprice0['last'])
    
    lastprice1=exchange.fetch_ticker(df1['symbol'][0])
    lastp1=float(lastprice1['last'])
    
    lastprice2=exchange.fetch_ticker(df2['symbol'][0])
    lastp2=float(lastprice2['last'])
    
    lastprice3=exchange.fetch_ticker(df3['symbol'][0])
    lastp3=float(lastprice3['last'])
    
    lastprice4=exchange.fetch_ticker(df4['symbol'][0])
    lastp4=float(lastprice4['last'])
    
    lastprice5=exchange.fetch_ticker(df5['symbol'][0])
    lastp5=float(lastprice5['last'])
    
    
    
    return lastp0,lastp1,lastp2,lastp3,lastp4,lastp5
    
bo0=0
bo1=0
bo2=0
bo3=0
bo4=0
bo5=0
    
    
def buying(api,api2,howmuch,howmuch2,n0,n1,n2,n3,n4,n5):
    global bo0,bo1,bo2,bo3,bo4,bo5
    exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
     })
    exchange2=ccxt.binance({
               'apiKey':api2.apiKey,
               'secret':api2.secretKey
    
    })    
    syms=getcoin()
    blc0,blc1,blc2,blc3,blc4,blc5,usdt=getallcoinsbalance(api,syms)
    resh,blnc,kn=balance(api)
    blx0,blx1,blx2,blx3,blx4,blx5,usdtx=getallcoinsbalance(api2,syms)
    df0,df1,df2,df3,df4,df5,TA0,TA1,TA2,TA3,TA4,TA5=getdata(api,'5m',55)
    x0=buycond(df0,TA0)
    x1=buycond(df1,TA1)
    x2=buycond(df2,TA2)
    x3=buycond(df3,TA3)
    x4=buycond(df4,TA4)
    x5=buycond(df5,TA5)
    lastp0,lastp1,lastp2,lastp3,lastp4,lastp5= lastprices(api)
    s0=df0['symbol'][0]
    s1=df1['symbol'][0]
    s2=df2['symbol'][0]
    s3=df3['symbol'][0]
    s4=df4['symbol'][0]
    s5=df5['symbol'][0]
    print('testing buying conditions on all coins')
    blc0=blc0*lastp0
    blc1=blc1*lastp1
    blc2=blc2*lastp2
    blc3=blc3*lastp3
    blc4=blc4*lastp4
    blc5=blc5*lastp5
    
    blx0=blx0*lastp0
    blx1=blx1*lastp1
    blx2=blx2*lastp2
    blx3=blx3*lastp3
    blx4=blx4*lastp4
    blx5=blx5*lastp5
    
    dfbtc,TAbtc=barr(exchange,'BTC/USDT','1m',55)
    nbtc=buycondbtc(dfbtc,TAbtc)
    if nbtc==1:
        print('btc conditions good')

    
    if  nbtc==1 and usdt>16 and x0==1 and blc0<50:
        bo0=exchange.create_market_buy_order(s0, howmuch/lastp0)
        bo0=bo0['info']['fills'][0]['price']
        print('coin',s0,'buyed at', bo0)
    
    usdt=usdtbl(api)
    if  nbtc==1 and  usdt>16 and x1==1 and blc1<50:
        bo1=exchange.create_market_buy_order(s1, howmuch/lastp1)
        bo1=bo1['info']['fills'][0]['price']
        print('coin',s1,'buyed at', bo1)
        
    usdt=usdtbl(api)    
    if  nbtc==1 and  usdt>16 and x2==1 and blc2<50:
        bo2=exchange.create_market_buy_order(s2, howmuch/lastp2)
        bo2=bo2['info']['fills'][0]['price']
        print('coin',s2,'buyed at', bo2)
        
    usdt=usdtbl(api)    
    if   nbtc==1 and usdt>16 and x3==1 and blc3<50:
        bo3=exchange.create_market_buy_order(s3, howmuch/lastp3)
        bo3=bo3['info']['fills'][0]['price']
        print('coin',s3,'buyed at', bo3)
    usdt=usdtbl(api)
    
    if   nbtc==1 and usdt>16 and x4==1 and blc4<50:
        bo4=exchange.create_market_buy_order(s4, howmuch/lastp4)
        bo4=bo4['info']['fills'][0]['price']
        print('coin',s4,'buyed at', bo4)
    usdt=usdtbl(api)    
    
    if   nbtc==1 and usdt>16 and x5==1 and blc5<50:
        bo5=exchange.create_market_buy_order(s5, howmuch/lastp5)
        bo5=bo5['info']['fills'][0]['price']
        print('coin',s5,'buyed at', bo5)


###################
    
    if  nbtc==1 and usdtx>16 and x0==1 and blx0<50:
        bo0=exchange2.create_market_buy_order(s0, howmuch2/lastp0)
        bo0=bo0['info']['fills'][0]['price']
        print('coin',s0,'buyed at', bo0)
    
    usdt=usdtbl(api)
    if  nbtc==1 and  usdtx>16 and x1==1 and blx1<50:
        bo1=exchange2.create_market_buy_order(s1, howmuch2/lastp1)
        bo1=bo1['info']['fills'][0]['price']
        print('coin',s1,'buyed at', bo1)
        
    usdt=usdtbl(api)    
    if  nbtc==1 and  usdtx>16 and x2==1 and blx2<50:
        bo2=exchange2.create_market_buy_order(s2, howmuch2/lastp2)
        bo2=bo2['info']['fills'][0]['price']
        print('coin',s2,'buyed at', bo2)
        
    usdt=usdtbl(api)    
    if   nbtc==1 and usdtx>16 and x3==1 and blc3<50:
        bo3=exchange2.create_market_buy_order(s3, howmuch2/lastp3)
        bo3=bo3['info']['fills'][0]['price']
        print('coin',s3,'buyed at', bo3)
    usdt=usdtbl(api)
    
    if   nbtc==1 and usdtx>16 and x4==1 and blx4<50:
        bo4=exchange2.create_market_buy_order(s4, howmuch2/lastp4)
        bo4=bo4['info']['fills'][0]['price']
        print('coin',s4,'buyed at', bo4)
    usdt=usdtbl(api)    
    
    if   nbtc==1 and usdtx>16 and x5==1 and blx5<50:
        bo5=exchange2.create_market_buy_order(s5, howmuch2/lastp5)
        bo5=bo5['info']['fills'][0]['price']
        print('coin',s5,'buyed at', bo5)
        
    return float(bo0),float(bo1),float(bo2),float(bo3),float(bo4),float(bo5)


sellordre0=0
sellordre2=0
sellordre3=0
sellordre4=0
sellordre5=0
sellordre1=0
gan=1.02
loss=0.99

def selling(api,api2,bbo0,bbo1,bbo2,bbo3,bbo4,bbo5):
    exchange=ccxt.binance({
               'apiKey':api.apiKey,
               'secret':api.secretKey
    
     })
    exchange2=ccxt.binance({
               'apiKey':api2.apiKey,
               'secret':api2.secretKey
    
    })
    global gan,loss,sellordre0,sellordre1,sellordre2,sellordre3,sellordre4,sellordre5
    syms=getcoin()
    blc0,blc1,blc2,blc3,blc4,blc5,usdt=getallcoinsbalance(api,syms)
    blx0,blx1,blx2,blx3,blx4,blx5,usdt=getallcoinsbalance(api2,syms)
    resh,blnc,kn=balance(api)
    df0,df1,df2,df3,df4,df5,TA0,TA1,TA2,TA3,TA4,TA5=getdata(api,'5m',55)   
    lastp0,lastp1,lastp2,lastp3,lastp4,lastp5= lastprices(api)
    
    y0=sellcond(df0,TA0)
    y1=sellcond(df1,TA1)
    y2=sellcond(df2,TA2)
    y3=sellcond(df3,TA3)
    y4=sellcond(df4,TA4)
    y5=sellcond(df5,TA5)
   
    
    yy0=sellcond3(df0,TA0)
    yy1=sellcond3(df1,TA1)
    yy2=sellcond3(df2,TA2)
    yy3=sellcond3(df3,TA3)
    yy4=sellcond3(df4,TA4)
    yy5=sellcond3(df5,TA5)   
    
    
    
    blco0=blc0*lastp0
    blco1=blc1*lastp1
    blco2=blc2*lastp2
    blco3=blc3*lastp3
    blco4=blc4*lastp4
    blco5=blc5*lastp5
    
    blcx0=blx0*lastp0
    blcx1=blx1*lastp1
    blcx2=blx2*lastp2
    blcx3=blx3*lastp3
    blcx4=blx4*lastp4
    blcx5=blx5*lastp5
    
    
    s0=df0['symbol'][0]
    s1=df1['symbol'][0]
    s2=df2['symbol'][0]
    s3=df3['symbol'][0]
    s4=df4['symbol'][0]
    s5=df5['symbol'][0]
    
    dfbtc,TAbtc=barr(exchange,'BTC/USDT','1m',55)
    mbtc=sellcondbtc(dfbtc,TAbtc)
    
    if (y0==1 or mbtc==1 or yy0==1 or lastp0>=bbo0*1.06 or lastp0<bbo0*loss) and blco0>1 :
        sellordre0=exchange.createMarketSellOrder (s0, blc0)
        
        sellordre0=sellordre0['info']['fills'][0]['price']
        print('coin',s0,'selled at     ', sellordre0)
                  
    if (y1==1 or mbtc==1 or yy1==1 or lastp1>=bbo1*1.04 or lastp1<bbo1*loss) and  blco1>1:
        sellordre1=exchange.createMarketSellOrder (s1, blc1)
        
        sellordre1=sellordre1['info']['fills'][0]['price']
        print('coin',s1,'selled at     ', sellordre1)
        
        
    if (y2==1 or mbtc==1 or y2==1 or lastp2>=bbo2*1.03 or lastp2<bbo2*loss) and blco2>1:
        sellordre2=exchange.createMarketSellOrder (s2, blc2)
        sellordre2=sellordre2['info']['fills'][0]['price'] 
        print('coin',s2,'selled at      ', sellordre2)
    
    if (y3==1 or mbtc==1 or yy3==1 or lastp3>=bbo3*gan or lastp3<bbo3*loss) and blco3>1:
        sellordre3=exchange.createMarketSellOrder (s3, blc3)
        sellordre3=sellordre3['info']['fills'][0]['price']
        print('coin',s3,'selled at      ', sellordre3)
        
        
    if (y4==1 or mbtc==1 or yy4==1 or lastp4>=bbo4*gan or lastp4<bbo4*loss) and blco4>1:
        sellordre4=exchange.createMarketSellOrder (s4, blc4)
        sellordre4=sellordre4['info']['fills'][0]['price']
        print('coin',s4,'selled at     ', sellordre4)
        
        
    if (y5==1 or mbtc==1 or yy5==1 or lastp5>=bbo5*gan or lastp5<bbo5*loss) and blco5>1:
        sellordre5=exchange.createMarketSellOrder (s5, blc5)
        sellordre5=sellordre5['info']['fills'][0]['price']
        print('coin',s5,'selled at     ', sellordre5)
        
        
    ############################################
        
    if (y0==1 or mbtc==1 or yy0==1 or lastp0>=bbo0*1.06 or lastp0<bbo0*loss) and blcx0>1 :
        sellordre0=exchange2.createMarketSellOrder (s0, blx0)
        
        sellordre0=sellordre0['info']['fills'][0]['price']
        print('coin',s0,'selled at     ', sellordre0)
                  
    if (y1==1 or mbtc==1 or yy1==1 or lastp1>=bbo1*1.04 or lastp1<bbo1*loss) and  blcx1>1:
        sellordre1=exchange2.createMarketSellOrder (s1, blx1)
        
        sellordre1=sellordre1['info']['fills'][0]['price']
        print('coin',s1,'selled at     ', sellordre1)
        
        
    if (y2==1 or mbtc==1 or y2==1 or lastp2>=bbo2*1.03 or lastp2<bbo2*loss) and blcx2>1:
        sellordre2=exchange2.createMarketSellOrder (s2, blx2)
        sellordre2=sellordre2['info']['fills'][0]['price'] 
        print('coin',s2,'selled at      ', sellordre2)
    
    if (y3==1 or mbtc==1 or yy3==1 or lastp3>=bbo3*gan or lastp3<bbo3*loss) and blcx3>1:
        sellordre3=exchange2.createMarketSellOrder (s3, blx3)
        sellordre3=sellordre3['info']['fills'][0]['price']
        print('coin',s3,'selled at      ', sellordre3)
        
        
    if (y4==1 or mbtc==1 or yy4==1 or lastp4>=bbo4*gan or lastp4<bbo4*loss) and blcx4>1:
        sellordre4=exchange2.createMarketSellOrder (s4, blx4)
        sellordre4=sellordre4['info']['fills'][0]['price']
        print('coin',s4,'selled at     ', sellordre4)
        
        
    if (y5==1 or mbtc==1 or yy5==1 or lastp5>=bbo5*gan or lastp5<bbo5*loss) and blcx5>1:
        sellordre5=exchange2.createMarketSellOrder (s5, blx5)
        sellordre5=sellordre5['info']['fills'][0]['price']
        print('coin',s5,'selled at     ', sellordre5)
    
    print('waitng for selling if the coin was buyed')
    return sellordre0,sellordre1,sellordre2,sellordre3,sellordre4,sellordre5
        


        
dl=0 

while True or xn==1:
    try:
        xn=0 
        bo0,bo1,bo2,bo3,bo4,bo5=buying(keys,keys2,40,40,0,0,0,0,0,0)

        sleep(10)
        selling(keys,keys2,bo0,bo1,bo2,bo3,bo4,bo5)
        

        sleep(10)
        dl=dl+1
        if dl==150:
            sellingbot(keys)
            sellingbot(keys2)
            dl=0
    
    
    except:
        print('error')
        xn=1
        
        bo0,bo1,bo2,bo3,bo4,bo5=buying(keys,keys2,40,40,0,0,0,0,0,0)

        sleep(10)
        selling(keys,keys2,bo0,bo1,bo2,bo3,bo4,bo5)
        

        sleep(10)
        dl=dl+1
        if dl==150:
            sellingbot(keys)
            sellingbot(keys2)
            dl=0


            
        
        
        


    