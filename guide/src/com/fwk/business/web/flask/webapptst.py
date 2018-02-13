# -- coding: utf-8 --
# 기존에 작성한 hello.py에 추가 하였다.

from flask import Flask
app = Flask(__name__)

#context root
@app.route('/')
def hello_world():
    return 'Hello World!'

# String 타입의 username 파라메터
# http://localhost:5000/user/사용자명
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

# int 타입의 post_id 파라메터
# http://localhost:5000/post/19
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

# float 타입의 pi 파라메터
# http://localhost:5000/circle/3.14
@app.route('/circle/<float:pi>')
def show_pi(pi):
    # show the post with the given id, the id is an integer
    return 'PI %f' % pi

# path 타입의 path 파라메터
# http://localhost:5000/path/path/test/kkk/
@app.route('/path/<path:path>')
def show_path(path):
    # show the post with the given id, the id is an integer
    return 'path %s' % path

if __name__ == '__main__':
    app.run()