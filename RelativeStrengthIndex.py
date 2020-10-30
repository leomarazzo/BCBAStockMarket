import itertools
import datetime
import ExponentialMovingAverage
import DatabaseActions
import pandas as pd

def RSI(historico, periodo):
    rsis = {}
    if len(historico.keys()) >= periodo:
        positives = []
        negatives = []
        dates = list(historico.keys())
        prev = historico[dates[0]]['c']
        positives.append(0)
        negatives.append(0)
        for i in range(1, len(dates)):
            date = dates[i]
            today = historico[date]['c']
            if (today > prev):
                positives.append(today-prev)
                negatives.append(0)
            elif (today < prev):
                positives.append(0)
                negatives.append(abs(today-prev))
            else:
                positives.append(0)
                negatives.append(0)
            prev = today

        avgGain = sum(positives[:periodo]) / periodo
        avgLoss = sum(negatives[:periodo]) / periodo
        try:
            RS = avgGain / avgLoss
            rsi = 100 - (100 / (1+ RS))
        except:
            rsi = 100
        rsis[datetime.datetime.fromisoformat(dates[periodo-1])] = rsi
        for i in range(periodo, len(dates)):
            try:
                avgGain = ((avgGain * 13) + positives[i]) / 14
                avgLoss = ((avgLoss * 13) + negatives[i]) / 14
                RS = avgGain / avgLoss
                rsi = 100 - (100 / (1+ RS))
            except:
                rsi = 100
            rsis[datetime.datetime.fromisoformat(dates[i])] = rsi

    return rsis

