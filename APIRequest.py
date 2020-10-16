import http.client
import json
import datetime
from dateutil import tz
import urllib
import time
import calendar
import DatabaseActions
import Logs
import sys


def ConnectToAPI(symbol, datefrom, resolution):
    logger = Logs.setup_logger("ConnectToAPI", "Logs/APIRequest.log", console=False)
    try:
        logger.info
        datefrom = datefrom.replace(
            tzinfo=tz.tzlocal()).astimezone(tz.tzutc()).replace(hour=21, minute=00, second=00)
        
        if datetime.datetime.now().hour < 17:
            toDate = datetime.datetime.today().replace(
            tzinfo=tz.tzlocal()).astimezone(tz.tzutc()).replace(hour=21, minute=00, second=00) - datetime.timedelta(days = 1)
        else:
            toDate = datetime.datetime.today().replace(
            tzinfo=tz.tzlocal()).astimezone(tz.tzutc()).replace(hour=21, minute=00, second=00)
        

        fromTimeStamp = int(calendar.timegm(datefrom.timetuple()))
        toTimeStamp = int(calendar.timegm(toDate.timetuple()))

        conn = http.client.HTTPConnection("www.invertironline.com")
        args = {"symbolName": symbol, "exchange": "BCBA", "resolution": resolution,
                "from": fromTimeStamp, "to": toTimeStamp}
        parameters = urllib.parse.urlencode(args)
        endpoint = "/api/cotizaciones/history?{}".format(parameters)

        logger.info("Requesting data {}".format(endpoint))

        conn.request("GET", endpoint)

        res = conn.getresponse()
        data = res.read()
        info = json.loads(data.decode("utf-8"))
        info = info["bars"]
        
        conn.close()

        if not(info):
            return True

        for entry in info:
            t = entry["time"]
            o = entry["open"]
            c = entry["close"]
            h = entry["high"]
            l = entry["low"]
            dateandtime = datetime.datetime.utcfromtimestamp(t)
            date = str(dateandtime.date().isoformat())
            DatabaseActions.insertToDatabase(
                date, symbol, o, h, l, c)
        
        logger.info("Data requested and sent")
        return False
    except:
        logger.error("Error requesting data and sending it to database")
        return False


def scrapping(symbol):
    logger = Logs.setup_logger("scrapping", "Logs/APIRequest.log", console=False)
    try:
        lastDate = DatabaseActions.getLastDate(symbol)
        if datetime.datetime.now().hour < 17:
            day = datetime.datetime.today().date() - datetime.timedelta(days = 1)
        else:
            day = datetime.datetime.today().date()

        empty = False
        while (lastDate < day.isoformat() and not(empty)):
            if len(lastDate) > 0:
                empty = ConnectToAPI(
                    symbol, datetime.datetime.fromisoformat(lastDate), "D")
            else:
                empty = ConnectToAPI(symbol, datetime.datetime(1900, 1, 1), "D")
            lastDate = DatabaseActions.getLastDate(symbol)
    except:
        logger.error(sys.exc_info()[1])
