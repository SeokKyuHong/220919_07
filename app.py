
from os import lseek
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import hashlib
import jwt
import datetime as dt
import time
from crypt import methods
from turtle import title

client = MongoClient('mongodb://SecondWind:clsgowlrlfqkfo@13.125.11.60', 27017)
db = client.db_00_07

app = Flask(__name__)

##############
###홍석규#######
# 회원가입 페이지 불러오기
@app.route('/signup', methods=['GET'])
def signup_read() :
    return render_template("signup.html")

# 회원가입 데이터 전송
@app.route('/signup', methods=['POST'])
def signup_post() :

    url_id = request.form['url_id'] 
    url_pw = request.form['url_pw'] 
    url_pw2 = request.form['url_pw2']
    url_name = request.form['url_name'] 

    article = {'id': url_id, 'pw': url_pw, 'name': url_name}
    
    db.user.insert_one(article)
    return jsonify({'result': 'success', 'msg': '가입완료'})

    # id_list = list(db.user.find({},{'_id':0, }))
    # id_list2 = db.user.find_one({'id': ''})
    # print(id_list)
    # id_list_len = len(id_list)
    # print(id_list_len)

# 회원가입 성공하면 로그인 페이지로 보내줌
# @app.route('/', methods=['GET'])
# def main_read() :
#     return render_template("main.html")

# 실시간 아이디 확인
@app.route('/id_check', methods=['POST'])
def id_check() :
    url_id = request.form['url_id']
    id_list = list(db.user.find({},{'_id':0, }))
    # id_list2 = db.user.find_one({'id': ''})
    # print(id_list)
    id_list_len = len(id_list)
    # print(id_list_len)
    
    for i in range(id_list_len):
        
        id_se = id_list[i]['id']
        if id_se == url_id:
            return jsonify({'result': 'success'})
            
        else:
            print()
    
    return jsonify({'result': 'bb'})       
        

###################
####### 최연준#######
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

# API 역할을 하는 부분
@app.route('/login', methods=['POST'])
def login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    # pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    result = db.user.find_one({'id': id_receive, 'pw': pw_receive})
    SECRET_KEY = 'this is key'
    if result is not None:
        payload = {
            'id': id_receive
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')


        return jsonify({'result': 'success', 'token': token})

    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/board/board', methods=['GET'])
def board():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        SECRET_KEY = 'this is key'
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        return render_template('board.html')
    else :
        return render_template('main.html')  
    
    
##############
###노유나#######


#Read Board
@app.route('/board', methods=['GET'])
def read_board():
    boards = list(db.boards.find({},{'_id':False}))
    return render_template("board/board.html", boards=boards)


#Create Board
@app.route('/createBoard', methods=['GET'])
def create_board():
    return render_template("board/createBoard.html")

#Ureate Board (미루자)

#Delete Board (미루자)

#페이징(노유나)

#게시판 늘리기(최연준)

#댓글 작성(홍석규)

#댓글 뷰(홍석규)

#대댓글 (홍석규)



if __name__ == '__main__':
    app.run('0.0.0.0',port=5005,debug=True)
