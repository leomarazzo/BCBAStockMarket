import http.client
import json
import datetime
from dateutil import tz
import urllib
import time
import calendar
import DatabaseActions


def ConnectToAPI(symbol, datefrom, resolution):
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
    conn.request("GET", endpoint)

    res = conn.getresponse()
    data = res.read()
    info = json.loads(data.decode("utf-8"))
    json.dump(info,open("test.json", 'w'))
    info = info["bars"]
    
    conn.close()

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


def scrapping(symbol):
    lastDate = DatabaseActions.getLastDate(symbol)
    if datetime.datetime.now().hour < 17:
        day = datetime.datetime.today().date() - datetime.timedelta(days = 1)
    else:
        day = datetime.datetime.today().date()

    while (lastDate < day.isoformat()):
        if len(lastDate) > 0:
            ConnectToAPI(
                symbol, datetime.datetime.fromisoformat(lastDate), "D")
        else:
            ConnectToAPI(symbol, datetime.datetime(1800, 1, 1), "D")
        lastDate = DatabaseActions.getLastDate(symbol)
