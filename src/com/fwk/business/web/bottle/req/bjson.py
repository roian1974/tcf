from bottle import Bottle, route, run, static_file, template
import time

HOST = 'localhost'

@route('/api/status')
def api_status():
    return {'status':'online', 'servertime':time.time()}

@route('/book/', method='GET')
def book(id):
    return {'id':id, 'name':'The Book Thief'}

run(host=HOST, port=8080, debug=True)
