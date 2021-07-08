import APIRequest
import DatabaseActions
import pandas as pd
import datetime
import ExponentialMovingAverage
import RelativeStrengthIndex
import SimulationEMAndRSI
import SimulationStoch
import TechnicalAnalysis
import SimulationEMA
import Logs
import os
import sys
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
from matplotlib.pylab import date2num

def actualizar():
    symbols = input("Input a symbol or many separated by comma (Input ALL to update all symbols): ")
    if symbols.upper() == "ALL":
        symbols = DatabaseActions.getAll()
    else:
        symbols = symbols.split(",")
    for symbol in symbols:
        APIRequest.scrapping(symbol)


def historico():
    symbol = input("Input a symbol: ")
    historico = DatabaseActions.getHistoric(symbol)
    historicDF = {}
    for key in historico:
        historicDF[datetime.datetime.fromisoformat(key)] = historico[key]
    df = pd.DataFrame.from_dict(historicDF, orient='index').tail(50).rename(
        columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close'})
    
    op = input("¿Agregar RSI? S/N: ")
    if op.lower() == 's':
        titulo = 'RSI'
        periodo = int(input("Ingrese el periodo: "))
        RSI = RelativeStrengthIndex.RSI(historico, periodo)
        df[titulo] = df.index.to_series().map(RSI)
    

    op = input("¿Agregar EMA? S/N: ")
    while op.lower() == 's':
        titulo = input("Ingrese un titulo para la EMA: ")
        periodo = int(input("Ingrese el periodo: "))
        EMAS = ExponentialMovingAverage.EMA(historico, periodo)
        df[titulo] = df.index.to_series().map(EMAS)
        op = input("¿Agregar otra EMA? S/N: ")
    
    print(df)
    data = df.tail(100)
    columns = list(data.columns)[4:]
    fig = plt.figure()
    fig.set_size_inches((20, 16))
    ax_candle = fig.add_axes((0, 0.05, 1, 0.9))
    ax_candle.xaxis_date()
    if 'RSI' in columns:
        ax_candle = fig.add_axes((0, 0.30, 1, 0.7))
        ax_rsi = fig.add_axes((0, 0.05, 1, 0.2), sharex=ax_candle)
        ax_rsi.set_ylabel("(%)")
        ax_rsi.plot(data.index, [70] * len(data.index), label="overbought")
        ax_rsi.plot(data.index, [30] * len(data.index), label="oversold")
        ax_rsi.plot(data.index, data["RSI"], label="RSI")
        ax_rsi.legend(loc="center left")
    
    ohlc = []
    for date, row in data.iterrows():
        Open, High, Low, Close = row[:4]
        ohlc.append([date2num(date), Open, High, Low, Close])

    for column in columns:
        if column != 'RSI':
            ax_candle.plot(data.index, data[column], label=column)
    candlestick_ohlc(ax_candle, ohlc, colorup="g", colordown="r")
    ax_candle.legend()
    plt.show()
    

def SimulacionEMAandRSI():
    symbols = input("Input a symbol or many separated by comma (Input ALL to Simulate for all symbols): ")
    if symbols.upper() == "ALL":
        symbols = DatabaseActions.getAll()
    else:
        symbols = symbols.split(",")
    for symbol in symbols:
        historico = DatabaseActions.getHistoric(symbol)
        SimulationEMAndRSI.simular(symbol,historico)

def SimulacionEMA():
    symbols = input("Input a symbol or many separated by comma (Input ALL to Simulate for all symbols): ")
    if symbols.upper() == "ALL":
        symbols = DatabaseActions.getAll()
    else:
        symbols = symbols.split(",")
    for symbol in symbols:
        historico = DatabaseActions.getHistoric(symbol)
        SimulationEMA.simular(symbol,historico)

def SimulacionStoch():
    symbols = input("Input a symbol or many separated by comma (Input ALL to Simulate for all symbols): ")
    if symbols.upper() == "ALL":
        symbols = DatabaseActions.getAll()
    else:
        symbols = symbols.split(",")
    for symbol in symbols:
        historico = DatabaseActions.getHistoric(symbol)
        SimulationStoch.simular(symbol,historico)
    
def GraphicsTechnicalAnalysis():
    symbols = input("Input a symbol or many separated by comma(Input ALL to Calculate for all symbols): ")
    if symbols.upper() == "ALL":
        symbols = DatabaseActions.getAll()
    else:
        symbols = symbols.split(",")
    for symbol in symbols:    
        historic = DatabaseActions.getHistoric(symbol)
        TechnicalAnalysis.GraphicsStoch(historic, symbol, parameters)

def params():
    symbol = input("Input a symbol (Input ALL to show for all symbols): ").upper()
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        if symbol == "ALL":
            print(parameters)
        elif symbol in list(parameters.index):
            print(parameters.loc[symbol])
        else:
            print("Symbol not in parameters.xlsx")

if __name__ == "__main__":
    if (not(os.path.exists("Logs"))):
        os.makedirs("Logs")
    if (not(os.path.exists("Graphics"))):
        os.makedirs("Graphics")
    else:
        for path in os.listdir("Graphics"):
            os.remove(os.path.join("Graphics", path))
    if (not(os.path.exists("Simulations"))):
        os.makedirs("Simulations")
    else:
        for path in os.listdir("Simulations"):
            os.remove(os.path.join("Simulations", path))
    try:
        DatabaseActions.testConnection()
    except:
        raise Exception("Error connecting to database. Please check the connection string and the server connection.")
    logger = Logs.setup_logger("scrapping", "Logs/APIRequest.log")
    op = '1'
    parameters = pd.read_excel('Parameters.xlsx')
    parameters = parameters.set_index('Simbolo')
    
    while op.lower() != 'q':
        print("Select an option")
        print("1 - Update Symbol")
        print("2 - Show historic data")
        print("3 - Create technical analysis graphics with saved parameters")
        print("4 - Simulate Exponential Moving Average Crossover")
        print("5 - Simulate Exponential Moving Average Crossover & Relative Strength Index")
        print("6 - Simulate Stochastic ocillator")
        print("7 - Show Stochastic parameters")
        print("q - Quit")
        print("")
        op = input("Enter an option: ")
        switcher = {
            '1': actualizar,
            '2': historico,
            '3': GraphicsTechnicalAnalysis,
            '4': SimulacionEMA,
            '5': SimulacionEMAandRSI,
            '6': SimulacionStoch,
            '7': params
        }
        func = switcher.get(op, lambda: "Invalid option")
        try:
            func()
        except Exception:
            logger.error(sys.exc_info()[1])
