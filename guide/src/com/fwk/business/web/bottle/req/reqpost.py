import requests
import json

a = 'Hello'
b = 'K'

http = 'http://localhost:8080/' + a +'/' + b
print (http)

# get
# r = requests.get(http)

# post
h = {'content-type': 'application/json'}
res = requests.post(http, headers=h)

print ('res.json().get("time") = %s' %(res.json().get('time')))
print ('res.json().get("g") = %s' %(res.json().get("g")))

print ('res = %s' %(res))