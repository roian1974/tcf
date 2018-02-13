import bottle
import json
from src.com.fwk.business.util.reflection import reflection
from src.com.fwk.business.web.bottle.action import tcfaction

app = bottle.Bottle()

mythings = ['apple', 'orange', 'banana', 'peach']

@app.route('/')
def home_page():
    fruit = bottle.request.get_cookie("fruit")
    name = 'World'
    return bottle.template("./tpl/welcome", { 'username':"roian", 'things': mythings, 'like': fruit, 'name':'roian'})


#--------------------
# http://localhost:8080/login
@app.route ('/login', method = 'GET') # or @get ( '/ login')
def login () :
    username = bottle.request.query.get('user')
    password = bottle.request.query.get( 'pass')

    #GET 아무것도 전달되지 않을 때는 username, password에 아무것도 넣지
    username = "" if username is None else username
    password = "" if password is None else password

    return bottle.template("./tpl/login.tpl", {})

@app.route ('/login' ,method = 'POST') # or @post ( '/ post')
def dologin () :
    username = bottle.request.forms.get( 'username')
    password = bottle.request.forms.get( 'password')
    return bottle.template("./tpl/loginrtn.tpl", {'username':username,'password':password})
    # return "{username} {password}".format (username = username, password = password)


# http://localhost:8080/html/tcfaction.html
@app.route('/html/<fname>')
def gethtml(fname='roian'):
    fname = './html/' + fname
    return bottle.template(fname, )

@app.route ('/action' ,method = 'POST') # or @post ('/post')
def action() :
    service = bottle.request.forms.get( 'service')
    program = bottle.request.forms.get( 'hostprog')
    data1 = bottle.request.forms.get( 'data1')
    data2 = bottle.request.forms.get('data2')

    res = tcfaction.action(service,program,data1,data2)
    return bottle.template("./tpl/tcfaction.tpl", {'svcname': service, "hostprog": program, 'outdata':str(res)})
    # return str(res)

# http://localhost:8080/sp_commo/COM1000/kk=1,jj=2
@app.route('/<action>/<name>/<parameter>')
def caction(action,name,parameter):
    svcname = action
    hostprog = name
    argv = parameter


    print(parameter.split('=')[1])
    argv = ['tcf_sp_commo', svcname, hostprog, parameter.split('=')[1]]
    res = reflection.reflection_argv('src.com.fwk.business.tcf.tcf_sp_commo', 'main',argv)

    return str(res)


# http://localhost:8080/html/tcfaction.html
@app.route('/joblist')
def getlistjob(joblist='111'):

    return bottle.template("./tpl/joblist.tpl" , )

# http://localhost:8080/html/tcfaction.html
@app.route('/list')
def getlist():


    argv = ['tcf_sp_commo', 'sp_commo', 'COM1000']
    res = reflection.reflection_argv('src.com.fwk.business.tcf.tcf_sp_commo', 'main',argv)


    lst = res['outdata'][0][0]

    res = []
    for val in lst :

        print('len--',val)

        if len(val) == 0 :
            continue
        l = ( val[0], 'jws', val[1][:10], '20101010', 10)
        res.append(l)

    lst = [('1','jws','emotion','20120101',100),('1','jws','emotion','20120101',100),('1','jws','emotion','20120101',100)]
    # return bottle.template("./tpl/table_list.tpl" , tdic=lst)

    return bottle.template("./tpl/table_list.tpl" , tdic=res)



bottle.debug(True)
app.run(host='localhost', port=8080)

