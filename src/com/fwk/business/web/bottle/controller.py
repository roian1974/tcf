import bottle
import json
from src.com.fwk.business.tcf import tcf_sp_commo
from src.com.fwk.business.util.reflection import reflection


mythings = ['apple', 'orange', 'banana', 'peach']

@bottle.route('/')
def home_page():
    fruit = bottle.request.get_cookie("fruit")
    print('/')
    return bottle.template("hello-world", username="roian", things=mythings, like=fruit)


@bottle.post('/favorite_fruits')
def favorite_fruits():
    fruit = bottle.request.forms.get('fruit')

    print('-------------')
    if (fruit == None or fruit == ""):
        fruit = "No Fruit Selected"

    bottle.response.set_cookie('fruit', fruit)


    return bottle.template("fruit.tpl", {'fruit': fruit})

# <body>
#     Your like {{fruit}}
# </body>

@bottle.route('/favorite_fruits1')
def favorite_fruits1():
    fruit = bottle.request.forms.get('fruit')

    print('-------------')
    if (fruit == None or fruit == ""):
        fruit = "No Fruit Selected"

    bottle.response.set_cookie('fruit', fruit)


    return bottle.template("fruit.tpl", {'fruit': fruit})


# http://localhost:8080/hello/roian
@bottle.route('/hello/<name>')
def greet(name='Stranger'):
    return bottle.template('Hello {{name}}, how are you?', name=name)


# http://localhost:8080/tcf/sp_commo
@bottle.route('/tcf/<name>')
def tcf(name='roian'):
    argv = ['tcf_sp_commo',name,'COM1000']
    tcf_sp_commo.main(argv)

    return bottle.template('tcf.tpl', {'name_var': argv[0]})
# <body>
#     Your like {{fruit}}
# </body>


# http://localhost:8080/getaction?svcname=sp_commo&hostname=COM1000
@bottle.route('/getaction/:')
def getaction(fname='roian'):
    print("------------------")
    svcname = bottle.request.get('svcname')
    hostname = bottle.request.get('hostname')
    print(svcname,hostname)

    return bottle.template(fname, )


# http://localhost:8080/html/action.html
@bottle.route('/html/<fname>')
def gethtml2(fname='roian'):
    print( '--fname',fname)
    return bottle.template(fname, )


# http://localhost:8080/formhtml/action.html
@bottle.route('/formhtml/<fname1>')
def gethtml(fname1='roian'):
    print( '--fname1',fname1)
    fname1 = './html/' + fname1
    return bottle.template(fname1, )

@bottle.post('/action')
def action():
    svcname = svr_name = bottle.request.forms.get('service_name')
    host_name = bottle.request.forms.get('host_program')
    val2 = bottle.request.forms.get('upload')

    argv = ['tcf_sp_commo',svcname,host_name]
    reflection.reflection_argv('src.com.fwk.business.tcf.tcf_sp_commo', 'main',argv)

    return bottle.template("action.tpl", {'svcname': svr_name, "hostprog" : host_name})


@bottle.post('/formaction')
def action1():
    name = bottle.request.forms.get('name')
    print('====nna',name)
    return bottle.template("action.tpl", {'svcname': name, "hostprog" : name})

#--------------------
# http://localhost:8080/login
@bottle.route ('/login', method = 'GET') # or @get ( '/ login')
def login () :
    username = bottle.request.query.get('user')
    password = bottle.request.query.get( 'pass')

    #GET 아무것도 전달되지 않을 때는 username, password에 아무것도 넣지
    username = "" if username is None else username
    password = "" if password is None else password

    return bottle.template("login.tpl", {})

    # return '<html><body>\
    # <form action = "/login" method = "post">     \
    #     Username: <input name = "username" type = "text" value = "{username}" />     \
    #     Password: <input name = "password" type = "password" value = "{password}" />     \
    #     <input value = "Login" type = "submit" /> \
    # </form></body>'. format (username = username, password = password)



@bottle.route ('/login' ,method = 'POST') # or @post ( '/ post')
def do_login () :
    username = bottle.request. forms. get ( 'username')
    password = bottle.request. forms. get ( 'password')

    return "{username} {password}".format (username = username, password = password)


# http://localhost:8080/sp_commo/COM1000
# http://localhost:8080/sp_commo/COM1000/kk=1,jj=2
@bottle.route('/<action>')
@bottle.route('/<action>/<name>')
@bottle.route('/<action>/<name>/<parameter>')
def action(action,name,parameter):
    svcname = action
    hostprog = name
    argv = parameter

    argv = ['tcf_sp_commo',svcname,hostprog,parameter]
    res = reflection.reflection_argv('src.com.fwk.business.tcf.tcf_sp_commo', 'main',argv)


    rv = [{ "id": 1, "name": "Test Item 1" }, { "id": 2, "name": "Test Item 2" }]

    return dict(data=rv)



@bottle.route ('/jobaction' ,method = 'POST') # or @post ( '/ post')
def jobaction () :
    service = bottle.request.forms.get ( 'service')
    progrm = bottle.request.forms.get ( 'hostprog')
    data1 = bottle.request.forms.get ( 'data1')
    data2 = bottle.request.forms.get('data2')

    argv = ['tcf_sp_commo',service,progrm,data1,data2]
    res = reflection.reflection_argv('src.com.fwk.business.tcf.tcf_sp_commo', 'main',argv)

    return str(res)

@bottle.route('/hello')
@bottle.route('/hello/<name>')
@bottle.view('hello_template')
def hello(name='World'):
    return dict(name=name)



bottle.debug(True)
bottle.run(host='localhost', port=8080)

