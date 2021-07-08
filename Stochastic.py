import pandas as pd

def ocillator(historico, kperiod, ksmooth, dperiod):
    historico['p-high'] = historico['High'].rolling(kperiod).max()
    historico['p-low'] = historico['Low'].rolling(kperiod).min()
    historico['stochK'] = (historico['Close'] - historico['p-low'])*100/(historico['p-high'] - historico['p-low'])
    historico['stochK'] = historico['stochK'].rolling(ksmooth).mean()
    historico['stochD'] = historico['stochK'].rolling(dperiod).mean()
    return historico