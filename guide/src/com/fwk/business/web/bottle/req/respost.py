#!/usr/bin/python
from bottle import Bottle, request, BaseRequest
import datetime

app = Bottle()

@app.get('//')
def notification(greeting, name):
    t = datetime.date.today().ctime()
    gr = greeting + ' ' + name + '!'
    return {'time':t, 'g': gr}

@app.post('//')
def notification(greeting, name):
    t = datetime.date.today().ctime()
    gr = greeting + ' ' + name + '!'
    return {'time':t, 'g': gr}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)