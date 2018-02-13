# https://parkminkyu.github.io/python/flask/05-python-flask.html

# -- coding: utf-8 --
from src.com.fwk.business.web.flask.dao import shedulerdao
from flask import Flask, request, render_template

# -- coding: utf-8 --
# shedulerdao import
app = Flask(__name__)

# 기본 페이지 접속
@app.route("/")
def index():
    return render_template("index.html")

# schedule 처리 get/post로 접근가능
@app.route("/scheduler",methods=["GET","POST","PUT","DELETE"])
def scheduler():
    # 요청이 get이면
    print(request.method)
    if request.method == 'GET':
        # fullCalendar에서 start와 end를 yyyy-mm-dd 형식의 parameter로 넘겨준다.
        start = request.args.get('start')
        end = request.args.get('end')
        # shedulerdao.getScheduler에 start와 end를 Dictoionary형식으로 넘겨준다.
        return shedulerdao.getScheduler({'start':start , 'end' : end})

    #요청이 post면
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        title = request.form['title']
        allDay = request.form['allDay']

        # Dictoionary 형식의 schedule 변수를 만든다. 추후 parameter를 받게 수정예정
        schedule = {'title' : title, 'start' : start, 'end' : end, 'allDay' : allDay}
        # schedule을 입력한다.
        return  shedulerdao.setScheduler(schedule)

    #요청이 delete면
    if request.method == 'DELETE':
        id = request.form['id']
        return  shedulerdao.delScheduler(id)

    #요청이 put이면
    if request.method == 'PUT':

        schedule = request.form
        print(schedule)
        return shedulerdao.putScheduler(schedule)

if __name__ =='__main__':
    app.run(debug=True)