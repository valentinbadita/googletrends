import requests
import json
import sys
#===============================================================================
# Use bulk requests towards Google Trends for knowing about if the term is
# used in organic search
# Below the parameters which are self explanatory
# 1st step: get the response payload necessary for building the CSV with the keywords
#===============================================================================
def trends(kw, period='1-d'):
    hl = 'ro-RO'
    tz = '-180'
    keyword = kw
    geo = 'RO'
    time = 'now '+period
    
    # construct the payload 
    comparisonItem = [{'keyword':keyword,'geo':geo,'time':time}]
    
    reqRaw = {'comparisonItem':comparisonItem,'category':'0','property':''}
    
    #Json in a parameter
    req = json.dumps(reqRaw)
    
    #full payload is ready
    payload = { 'hl':hl,'tz':tz,'req':req,'tz':tz}
    
    #sending the get request
    getrequest = requests.get('https://trends.google.ro/trends/api/explore',params=payload);
    
    #test
    firstResponse = getrequest.content[4:]
    
    firstResponseJson = json.loads(firstResponse)
    
    # The 3rd element represents the data for Related Search widget
    reqwidget = firstResponseJson['widgets'][3]['request']
    reqwidgetJson = json.dumps(reqwidget)
    token = firstResponseJson['widgets'][3]['token']
    
    payloadFinal = { 'hl':hl,'tz':tz,'req':reqwidgetJson,'tz':tz,'token':token}
    
    #sending the final request
    getrequestFinal = requests.get('https://trends.google.ro/trends/api/widgetdata/relatedsearches/csv',params=payloadFinal);
    
    
    #test
    print(getrequestFinal.text)


if __name__ == '__main__':
    lenparam = len(sys.argv)
    if(lenparam==2):
    	trends(sys.argv[1])
    else:
    	trends(sys.argv[1],sys.argv[2])
    
