from bottle import route, run, static_file

@route('/')
def serve_homepage():
    return static_file('home.html', root='static/')

@route('/static/<filename:path>')
def st(filename):
    print(filename)
    return static_file(filename, root='./static')

run(host='localhost', port=8080)
