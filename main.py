# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 11:23:10 2021

@author: abdou
"""


from calculandordre import *

from time import time, sleep
import pandas as pd

lstp1=pd.DataFrame()
lstp2=pd.DataFrame()
lstp11=pd.DataFrame()
lstp22=pd.DataFrame()
import keys
import keys2

limit=55
howmuch=50
sl=0.995

gn=1.02
macdperiode=9

hi=pd.DataFrame([])
aa=pd.DataFrame([])

def main(key,f,listcoins):
   """mac=pd.read_csv('macdbacktestgain.csv',index_col=0)
  
   if rs['0'].iloc[0]<=0 or mac['0'].iloc[0]<=0:
      print('market is not good waiting ...')
      print('back test of the macd hist gain :',mac['0'].iloc[0],'%')
      sleep(60)"""

   
   ls=testandordre(key,listcoins,f,limit,howmuch,gn,sl,macdperiode,lstp1,lstp2) 
   aa=hi.append(ls)
   aa.to_csv('coinsforthissession.csv')
   print(aa)
   return aa

while True:
   maching=pd.read_csv('coins4h.csv',index_col=0)   
   filtredsymbols4h = [s for s in maching['0'] if "USDT" in s]
  

  
   maching2=pd.read_csv('coins1d.csv',index_col=0)   
   filtredsymbols1d = [s for s in maching2['0'] if "USDT" in s]
   
   maching3=pd.read_csv('coins1m.csv',index_col=0)   
   filtredsymbols1m = [s for s in maching3['0'] if "USDT" in s]
   

   #minf=main(keys2,'1m',filtredsymbols1m)
   lstp11=main(keys,'15m',filtredsymbols4h)
   
   

   #lstp22=main(keys,'5m',filtredsymbols1d)
   #lstp11=lstp11.append(lstp22)
   
   lstp11.to_csv('history.csv')
   sleep(300)
   