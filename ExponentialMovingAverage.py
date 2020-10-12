import itertools
import datetime


def SMA(series):
    SUM = 0
    for n in series:
        SUM += series[n]['c']
    return SUM / len(series)


def EMA(historico, periodo):
    emas = {}
    if len(historico.keys()) >= periodo:
        dates = list(historico.keys())
        for i in range(0, periodo-1):
            emas[datetime.datetime.fromisoformat(dates[i])] = 0

        EMAANT = SMA(dict(itertools.islice(historico.items(), periodo)))
        emas[datetime.datetime.fromisoformat(dates[periodo-1])] = EMAANT
        for i in range(periodo, len(dates)):
            EMAAC = historico[dates[i]]['c']*(2/(periodo + 1)) + EMAANT * \
                (1 - (2/(periodo + 1)))
            emas[datetime.datetime.fromisoformat(dates[i])] = EMAAC
            EMAANT = EMAAC
    return emas

