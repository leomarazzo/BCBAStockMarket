import pyodbc
import json
import Logs
import sys

def insertToDatabase(date, symbol, o, h, l, c):
    logger = Logs.setup_logger("insertToDatabase", "Logs/DatabaseActions.log")
    config = json.load(open("config.json"))
    st = config["st"]
    try:
        logger.info("Connectiong to database")
        cnxn = pyodbc.connect(st)
        cursor = cnxn.cursor()
    except:
        logger.error("Error connecting to database: {}".format(st.split(";")[1]))
        raise Exception("Error connecting to database")
    
    try:    
        sql_cmd = "Select * from Simbolos where Symbol = '{}' and date = '{}'".format(symbol, date)
        cursor.execute(sql_cmd)
        res = cursor.fetchone()
        if res == None:
            logger.info("Sending data to database: {:4>}, {:.3f}, {:.3f}, {:.3f}, {:.3f}".format(symbol, o, h, l, c))
            sql_cmd = "insert into Simbolos values ('{}', '{}',{},{},{},{})".format(date, symbol, o, h, l, c)
            cursor.execute(sql_cmd)
            cnxn.commit()
    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        print(sqlstate)
    except:
        logger.error("Error sending data to database: ".format(sys.exc_info()[1]))
        raise Exception("Error sending data")

def getLastDate(symbol):
    logger = Logs.setup_logger("getLastDate", "Logs/DatabaseActions.log")
    config = json.load(open("config.json"))
    st = config["st"]
    try:
        logger.info("Connecting to database")
        cnxn = pyodbc.connect(st)
        cursor = cnxn.cursor()
        logger.info("Getting last date for symbol: {}".format(symbol))
        sql_cmd = "Select MAX(Date) from Simbolos where Symbol = '{}'".format(symbol)
        cursor.execute(sql_cmd)
        res = cursor.fetchone()
        last = ''
        if res[0] != None:
            last = res[0]
        logger.info("Last date {}: {}".format(symbol, last))
        return last
    except:
        logger.error("Error connecting to database: {}".format(st.split(";")[1]))
        raise Exception("Error connecting to database")
    

def getHistoric(symbol):

    logger = Logs.setup_logger("getHistoric", "Logs/DatabaseActions.log")
    config = json.load(open("config.json"))
    st = config["st"]
    try:
        logger.info("Connectiong to database")
        cnxn = pyodbc.connect(st)
        cursor = cnxn.cursor()

        logger.info("Getting data for symbol: {}".format(symbol))
        sql_cmd = "Select * from Simbolos where symbol = '" + symbol + "'"
        cursor.execute(sql_cmd)

        historic = {}
        for row in cursor:
            historic[row[0]] = {'o': row[2], 'h': row[3], 'l': row[4], 'c': row[5] }
        return historic
    except:
        logger.error("Error connecting to database: {}".format(st.split(";")[1]))
        raise Exception("Error connecting to database")

    
    
        

