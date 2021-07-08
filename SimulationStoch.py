import Stochastic
import pandas as pd
import datetime
import os
import openpyxl
import sys
import Logs
import time


def simular(symbol, historico):

    logger = Logs.setup_logger(
        "Simulation", "Logs/SimulationStoch.log", console=True)

    try:
        tstart = time.time()
        logger.info("Simulation start: {}".format(symbol))
        output = pd.DataFrame(columns=["Period", "SmoothK", "SmoothD", "Average efficency", "Total trades", "Total efficency",
                                       "Efficencies averages", "Average Duration", "Positive trades", "Negative trades", "Efficency probability"])
        for i in range(2, 21):
            for j in range(1, 10):
                for k in range(2, 10):
                    logger.info(
                        "Simulating: {} --- {} --- {} --- {}".format(symbol, i, j, k))
                    DineroIncial = 10000
                    DineroDisponible = 20000
                    OperacionAbierta = False
                    abrirOperacion = False
                    cerrarOperacion = False
                    DineroInvertido = 0
                    CantidadComprada = 0
                    DineroFinal = 0
                    ContadorTrades = 0
                    ContadorTradesPositivos = 0
                    ContadorTradesNegativos = 0
                    SUMEficaciaOperacion = 0
                    SUMDiasOperacion = 0
                    fechaApertura = None
                    historicDF = {}
                    for key in historico:
                        historicDF[datetime.datetime.fromisoformat(
                            key)] = historico[key]
                    df = pd.DataFrame.from_dict(historicDF, orient='index').rename(
                        columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close'})
                    
                    df = Stochastic.ocillator(df, i, j, k)

                    df2 = df.tail(1000)

                    for index, row in df2.iterrows():
                        
                        indexant = df.index.get_loc(index) -1
                        K = row['stochK']
                        KAnt = df.iloc[indexant]['stochK']
                        D = row['stochD']
                        DAnt = df.iloc[indexant]['stochD']
                        


                        if ((not(OperacionAbierta)) and abrirOperacion):
                            precio = row['Open']
                            CantidadComprada = DineroDisponible // precio
                            DineroInvertido = precio * CantidadComprada
                            DineroDisponible -= DineroInvertido
                            fechaApertura = index
                            OperacionAbierta = True
                            abrirOperacion = False

                        abrirOperacion = ((not(OperacionAbierta)) and ((
                            K >= D) and (KAnt < DAnt)))

                        if (OperacionAbierta and cerrarOperacion):
                            precio = row['Open']
                            DiasOperacion = (index - fechaApertura).days
                            SUMDiasOperacion += DiasOperacion
                            DineroVenta = CantidadComprada * precio
                            if (DineroInvertido < DineroVenta):
                                ContadorTradesPositivos = ContadorTradesPositivos + 1
                            else:
                                ContadorTradesNegativos = ContadorTradesNegativos + 1
                            EficaciaOperacion = (
                                DineroVenta - DineroInvertido) / DineroInvertido
                            SUMEficaciaOperacion = SUMEficaciaOperacion + EficaciaOperacion
                            DineroDisponible = DineroDisponible + DineroVenta
                            DineroInvertido = 0
                            CantidadComprada = 0
                            ContadorTrades = ContadorTrades + 1
                            OperacionAbierta = False
                            cerrarOperacion = False

                        cerrarOperacion = (OperacionAbierta and (
                            (K < D) and (KAnt > DAnt)))

                    if (OperacionAbierta):
                        fecha = df.index[-1]
                        precio = df.tail(1)['Open']
                        DiasOperacion = (fecha - fechaApertura).days
                        DineroVenta = (CantidadComprada * precio).to_numpy()[0]
                        a = DineroInvertido < DineroVenta
                        if (a):
                            ContadorTradesPositivos = ContadorTradesPositivos + 1
                        else:
                            ContadorTradesNegativos = ContadorTradesNegativos + 1
                        EficaciaOperacion = (
                            DineroVenta - DineroInvertido) / DineroInvertido
                        SUMEficaciaOperacion = SUMEficaciaOperacion + EficaciaOperacion
                        DineroDisponible = DineroDisponible + DineroVenta
                        DineroInvertido = 0
                        CantidadComprada = 0
                        ContadorTrades = ContadorTrades + 1
                        OperacionAbierta = False

                    if (ContadorTrades > 0):
                        DineroFinal = DineroDisponible
                        EficiaTotal = (
                            DineroFinal - DineroIncial) / DineroIncial
                        EficaciaPromedio = EficiaTotal / ContadorTrades
                        PromedioEficacia = SUMEficaciaOperacion / ContadorTrades
                        ProbabilidadEficacia = ContadorTradesPositivos / ContadorTrades
                        PromedioDuracion = int(
                            SUMDiasOperacion / ContadorTrades)
                        if ContadorTrades > 5 and PromedioDuracion > 2 and PromedioDuracion < 40 and ProbabilidadEficacia > 0.5:
                            output = output.append({
                                "Period": i,
                                "SmoothK": j,
                                "SmoothD": k,
                                "Average efficency": EficaciaPromedio,
                                "Total trades": ContadorTrades,
                                "Total efficency": EficiaTotal,
                                "Efficencies averages": PromedioEficacia,
                                "Average Duration": PromedioDuracion,
                                "Positive trades": ContadorTradesPositivos,
                                "Negative trades": ContadorTradesNegativos,
                                "Efficency probability": ProbabilidadEficacia
                            }, ignore_index=True)
        output.sort_values(by='Total efficency', ascending=False).head(50)\
            .sort_values(by='Efficency probability', ascending=False)\
                .to_excel("Simulations/{}.xlsx".format(symbol))
        tend = time.time()
        duration = (tend - tstart) / 60
        logger.info("Simulation end: {}. Duration: {}".format(symbol, duration))
    except:
        logger.error("Error during simulation: {}".format(sys.exc_info()[1]))
