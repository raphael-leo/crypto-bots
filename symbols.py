# -*- coding: utf-8 -*-
"""
Created on Sun Jun 13 13:42:08 2021

@author: abdou
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 16:45:42 2021

@author: abdou
"""

#a=exchange.fetchTickers ()
#aa=pd.DataFrame([a])
#for x in aa:
   # print(x)
   # symbols=symbols.append(x)
    
#matching = [s for s in symbols[:][0] if "USDT" in s]
#https://www.tradingview.com/x/yTC7qzAL/

allsymbols=[ 'NEO/USDT',
 'QTUM/USDT',
 'ADA/USDT',
 'XRP/USDT',
 'IOTA/USDT',
 'XLM/USDT',
 'ONT/USDT',
 'TRX/USDT',
 'ICX/USDT',
 'NULS/USDT',
 'VET/USDT',
 'LINK/USDT',
 'WAVES/USDT',
 'BTT/USDT',
 'ONG/USDT',
 'HOT/USDT',
 'ZIL/USDT',
 'ZRX/USDT',
 'FET/USDT',
 'BAT/USDT',
 'XMR/USDT',
 'ZEC/USDT',
 'IOST/USDT',
 'CELR/USDT',
 'DASH/USDT',
 'NANO/USDT',
 'OMG/USDT',
 'THETA/USDT',
 'ENJ/USDT',
 'MITH/USDT',
 'MATIC/USDT',
 'ATOM/USDT',
 'TFUEL/USDT',
 'ONE/USDT',
 'FTM/USDT',
 'ALGO/USDT',
 'GTO/USDT',
 'DOGE/USDT',
 'DUSK/USDT',
 'ANKR/USDT',
 'WIN/USDT',
 'COS/USDT',
 'NPXS/USDT',
 'COCOS/USDT',
 'MTL/USDT',
 'TOMO/USDT',
 'PERL/USDT',
 'DENT/USDT',
 'MFT/USDT',
 'KEY/USDT',
 'DOCK/USDT',
 'WAN/USDT',
 'FUN/USDT',
 'CVC/USDT',
 'CHZ/USDT',
 'BAND/USDT',
 'BEAM/USDT',
 'XTZ/USDT',
 'REN/USDT',
 'RVN/USDT',
 'HC/USDT',
 'HBAR/USDT',
 'NKN/USDT',
 'STX/USDT',
 'KAVA/USDT',
 'ARPA/USDT',
 'IOTX/USDT',
 'RLC/USDT',
 'CTXC/USDT',
 'TROY/USDT',
 'FTT/USDT',
 'OGN/USDT',
 'DREP/USDT',
 'TCT/USDT',
 'WRX/USDT',
 'BTS/USDT',
 'LSK/USDT',
 'BNT/USDT',
 'LTO/USDT',
 'AION/USDT',
 'MBL/USDT',
 'COTI/USDT',
 'STPT/USDT',
 'WTC/USDT',
 'DATA/USDT',
 'SOL/USDT',
 'CTSI/USDT',
 'HIVE/USDT',
 'CHR/USDT',
 'GXS/USDT',
 'ARDR/USDT',
 'STMX/USDT',
 'KNC/USDT',
 'REP/USDT',
 'LRC/USDT',
 'PNT/USDT',
 'COMP/USDT',
 'ZEN/USDT',
 'SNX/USDT',
 'VTHO/USDT',
 'DGB/USDT',
 'SXP/USDT',
 'MKR/USDT',
 'DCR/USDT',
 'STORJ/USDT',
 'MANA/USDT',
 'YFI/USDT',
 'BAL/USDT',
 'BLZ/USDT',
 'IRIS/USDT',
 'KMD/USDT',
 'SRM/USDT',
 'ANT/USDT',
 'CRV/USDT',
 'SAND/USDT',
 'OCEAN/USDT',
 'NMR/USDT',
 'DOT/USDT',
 'LUNA/USDT',
 'RSR/USDT',
 'WNXM/USDT',
 'TRB/USDT',
 'BZRX/USDT',
 'KSM/USDT',
 'EGLD/USDT',
 'DIA/USDT',
 'RUNE/USDT',
 'FIO/USDT',
 'BEL/USDT',
 'WING/USDT',
 'UNI/USDT',
 'NBS/USDT',
 'OXT/USDT',
 'AVAX/USDT',
 'HNT/USDT',
 'FLM/USDT',
 'ORN/USDT',
 'UTK/USDT',
 'ALPHA/USDT',
 'AAVE/USDT',
 'NEAR/USDT',
 'FIL/USDT',
 'INJ/USDT',
 'AUDIO/USDT',
 'CTK/USDT',
 'AKRO/USDT',
 'AXS/USDT',
 'HARD/USDT',
 'DNT/USDT',
 'STRAX/USDT',
 'UNFI/USDT',
 'ROSE/USDT',
 'AVA/USDT',
 'XEM/USDT',
 'SKL/USDT',
 'GRT/USDT',
 'JUV/USDT',
 'PSG/USDT',
 '1INCH/USDT',
 'REEF/USDT',
 'OG/USDT',
 'ATM/USDT',
 'ASR/USDT',
 'CELO/USDT',
 'RIF/USDT',
 'TRU/USDT',
 'CKB/USDT',
 'TWT/USDT',
 'FIRO/USDT',
 'LIT/USDT',
 'SFP/USDT',
 'DODO/USDT',
 'CAKE/USDT',
 'ACM/USDT',
 'BADGER/USDT',
 'FIS/USDT',
 'OM/USDT',
 'POND/USDT',
 'DEGO/USDT',
 'ALICE/USDT',
 'LINA/USDT',
 'PERP/USDT',
 'RAMP/USDT',
 'SUPER/USDT',
 'CFX/USDT',
 'EPS/USDT',
 'AUTO/USDT',
 'TKO/USDT',
 'PUNDIX/USDT',
 'TLM/USDT',
 'BTG/USDT',
 'MIR/USDT',
 'BAR/USDT',
 'FORTH/USDT',
 'BAKE/USDT',
 'BURGER/USDT',
 'SLP/USDT',
 'SHIB/USDT',
 'ICP/USDT',
 'AR/USDT',
 'POLS/USDT',
 'MDX/USDT',
 'MASK/USDT',
 'LPT/USDT']