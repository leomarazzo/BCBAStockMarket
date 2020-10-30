import pandas as pd
import datetime
import ExponentialMovingAverage
import RelativeStrengthIndex
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num
import os
import Logs
import sys


def Graphics(historic, symbol, parameters):
    logger = Logs.setup_logger(
        "EMACrossover", "Logs/EMACrossover.log", console=False)
    try:
        periodoCorto = int(parameters.loc[symbol]['MMC'])
        periodoLargo = int(parameters.loc[symbol]['MML'])
        periodoRSI = int(parameters.loc[symbol]['RSI'])
        logger.info("Calculating EMA cross: {}, {}, {}".format(
            symbol, periodoCorto, periodoLargo))
        historicDF = {}
        for key in historic:
            historicDF[datetime.datetime.fromisoformat(key)] = historic[key]
        df = pd.DataFrame.from_dict(historicDF, orient='index').rename(
            columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close'})
        EMAc = ExponentialMovingAverage.EMA(historic, periodoCorto)
        df["EMA{}".format(periodoCorto)] = df.index.to_series().map(EMAc)
        EMAl = ExponentialMovingAverage.EMA(historic, periodoLargo)
        df["EMA{}".format(periodoLargo)] = df.index.to_series().map(EMAl)
        RSI = RelativeStrengthIndex.RSI(historic, periodoRSI)
        df['RSI'] = df.index.to_series().map(RSI)

        data = df.tail(30)
        EMAs = list(data.columns)[4:]
        fig = plt.figure()
        fig.set_size_inches((20, 16))
        ax_candle = fig.add_axes((0, 0.05, 1, 0.9))
        ax_candle = fig.add_axes((0, 0.30, 1, 0.7))
        ax_rsi = fig.add_axes((0, 0.05, 1, 0.2), sharex=ax_candle)
        ax_rsi.set_ylabel("(%)")
        ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")
        ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")
        ax_rsi.plot(data.index, data["RSI"], label="RSI")
        ax_rsi.legend(loc="center left")
        ax_candle.xaxis_date()
        ohlc = []
        for date, row in data.iterrows():
            Open, High, Low, Close = row[:4]
            ohlc.append([date2num(date), Open, High, Low, Close])

        for ema in EMAs:
            ax_candle.plot(data.index, data[ema], label=ema)
        candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r")
        ax_candle.legend()
        fig.savefig('Graphics\{}.png'.format(symbol))
        plt.close()
    except:
        logger.error(
            "Error calculating EMA cross: {}".format(sys.exc_info()[1]))
