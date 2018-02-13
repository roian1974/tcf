import requests
import json


def req_cli() :
    a = 'Hello'
    b = 'K'

    http = 'http://localhost:8080/' + a +'/' + b
    print (http)

    # get
    r = requests.get(http)

    print ('r.json().get("time") = %s' %(r.json().get('time')))
    print ('r.json().get("g") = %s' %(r.json().get("g")))

if __name__ == 'main' :
    req_cli()