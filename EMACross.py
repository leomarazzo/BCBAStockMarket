import pandas as pd
import datetime
import ExponentialMovingAverage
import mplfinance as mpf
import matplotlib.pyplot as plt
import os

def EMACrossover(historic, symbol, parameters):
    if (not(os.path.exists("Graphics"))):
        os.makedirs("Simulations")
    periodoCorto = int(parameters.loc[symbol]['MMC'])
    periodoLargo = int(parameters.loc[symbol]['MML'])
    historicDF = {}
    for key in historic:
        historicDF[datetime.datetime.fromisoformat(key)] = historic[key]
    df = pd.DataFrame.from_dict(historicDF, orient='index').rename(
        columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close'})
    EMAc = ExponentialMovingAverage.EMA(historic, periodoCorto)
    EMAl = ExponentialMovingAverage.EMA(historic, periodoLargo)
    dfc = pd.DataFrame.from_dict(EMAc, orient='index').tail(30)
    dfl = pd.DataFrame.from_dict(EMAl, orient='index').tail(30)
    
    apd = [mpf.make_addplot(dfc), mpf.make_addplot(dfl)]
    mpf.plot(df.tail(30), type='candle', addplot=apd, title=symbol,savefig=dict(fname='Graphics\{}.png'.format(symbol).replace("/", "-"),dpi=500,pad_inches=1), closefig=True)
    
    
