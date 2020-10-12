import pyodbc
import json

def insertToDatabase(date, symbol, o, h, l, c):
    config = json.load(open("config.json"))
    st = config["st"]
    cnxn = pyodbc.connect(st)
    cursor = cnxn.cursor()
    
    sql_cmd = "Select * from Simbolos where Symbol = '{}' and date = '{}'".format(symbol, date)
    cursor.execute(sql_cmd)
    res = cursor.fetchone()
    if res == None:
        print("Send to database: {:10}, {:10}, {:.3f}, {:.3f}, {:.3f}, {:.3f}".format(date, symbol, o, h, l, c))
        sql_cmd = "insert into Simbolos values ('{}', '{}',{},{},{},{})".format(date, symbol, o, h, l, c)
        cursor.execute(sql_cmd)
    cnxn.commit()

def getLastDate(symbol):
    config = json.load(open("config.json"))
    st = config["st"]
    cnxn = pyodbc.connect(st)
    cursor = cnxn.cursor()
    
    sql_cmd = "Select MAX(Date) from Simbolos where Symbol = '{}'".format(symbol)
    cursor.execute(sql_cmd)
    res = cursor.fetchone()
    last = ''
    if res[0] != None:
        last = res[0]
    
    return last
    

def getHistoric(symbol):
    config = json.load(open("config.json"))
    st = config["st"]
    cnxn = pyodbc.connect(st)
    cursor = cnxn.cursor()

    sql_cmd = "Select * from Simbolos where symbol = '" + symbol + "'"
    cursor.execute(sql_cmd)

    historic = {}
    for row in cursor:
        historic[row[0]] = {'o': row[2], 'h': row[3], 'l': row[4], 'c': row[5] }

    
    return historic
        

