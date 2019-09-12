import requests
import urllib
import json
import codecs
from datetime import datetime
from threading import Timer

def parse_api(url):
    #url='http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=036358422804c631581aca0621ae5418'
    response = urllib.request.urlopen(url)
    webContent = response.read()
    webContent = json.loads(webContent.decode('utf-8'))
    return webContent 

if __name__ == "__main__":
     for month in range(6,9):
        if month < 10:
            month='0'+str(month)
        else:
            month=str(month)
            for day in range(1,31):
                if day <10:
                    day='0'+str(day)
                else:
                    day=str(day)
                            
            url='https://www.timeanddate.com/scripts/cityajax.php?n=united-arab-emirates/dubai&mode=historic&hd=2017'+month+day+'&month='+str(int(month))+'&year=2017&json'

            # Call the api
            content=parse_api(url)

            # Print the results
            print(len(content))
                              
            break
        break
    