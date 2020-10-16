import APIRequest
import DatabaseActions
import pandas as pd
import datetime
import mplfinance as mpf
import ExponentialMovingAverage
import SimEMA
import EMACross
import Logs
import os

def actualizar():
    symbols = input("Input a symbol or many separated by comma: ").split(",")
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
    print(df)
    mpf.plot(df, type='candle', title=symbol)


def EMA():
    symbol = input("Input a symbol: ")
    op = 's'
    historico = DatabaseActions.getHistoric(symbol)
    historicDF = {}
    for key in historico:
        historicDF[datetime.datetime.fromisoformat(key)] = historico[key]
    df = pd.DataFrame.from_dict(historicDF, orient='index').rename(
        columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close'})
    while op.lower() == 's':
        periodo = int(input("Ingrese el periodo: "))

        EMAS = ExponentialMovingAverage.EMA(historico, periodo)
        titulo = input("Ingrese un titulo para la EMA: ")
        df[titulo] = df.index.to_series().map(EMAS)

        op = input("¿Agregar otra EMA? S/N: ")
    print(df)

def SimulacionEMA():
    symbols = input("Input a symbol or many separated by comma: ").split(",")
    for symbol in symbols:
        historico = DatabaseActions.getHistoric(symbol)
        SimEMA.simular(symbol,historico)
    
def EMACrossover():
    symbols = input("Input a symbol or many separated by comma: ").split(",")
    parameters = pd.read_excel('Parameters.xlsx')
    parameters = parameters.set_index('Simbolo')
    for symbol in symbols:    
        historic = DatabaseActions.getHistoric(symbol)
        EMACross.EMACrossover(historic, symbol, parameters)

def params():
    parameters = pd.read_excel('Parameters.xlsx')
    parameters = parameters.sort_values(by='Simbolo')
    parameters = parameters.set_index('Simbolo')
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(parameters)

if __name__ == "__main__":
    op = '1'
    if (not(os.path.exists("Logs"))):
        os.makedirs("Logs")
    if (not(os.path.exists("Graphics"))):
        os.makedirs("Graphics")
    while op.lower() != 'q':
        print("Select an option")
        print("1 - Update Symbol")
        print("2 - Show historic data")
        print("3 - Calculate Exponential Moving Average")
        print("4 - Calculate Exponential Moving Average Crossover")
        print("5 - Simulate Exponential Moving Average Crossover")
        print("6 - Show EMA Crossover parameters")
        print("q - Quit")
        print("")
        op = input("Enter an option: ")
        switcher = {
            '1': actualizar,
            '2': historico,
            '3': EMA,
            '4': EMACrossover,
            '5': SimulacionEMA,
            '6': params
        }
        func = switcher.get(op, lambda: "Invalid option")
        func()
