from glob import escape
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import time
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb://SecondWind:clsgowlrlfqkfo@13.125.11.60', 27017)
db = client.db_00_07

# JWT 토큰을 만들 때 필요한 비밀문자열, 자유롭게 입력
# 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 가능
SECRET_KEY = 'SPARTA'

# JWT 패키지 사용 (설치: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 비밀번호 암호화를 위해
import hashlib


#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/')
def home():
    # boards = db.boards.find({})
    try:
        token_receive = request.cookies.get('mytoken')

        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        
        comments = list(db.comment.find({}, {'_id': False}))
            

    
        list_board = list(db.boards.find({}))
        for board in list_board:
            board['comment'] = []
            board['_id']=str(board['_id'])
            board['no']=str(board['_id'])
            for comment in comments:
                if comment['board_ojid'] == board['no']:
                    board['comment'].append(comment)
        # for i in range(0, len(list_board)-1):
        #     id = str(boards[i]['_id'])
        #     list_board[i]['no'] = id
            print("=============")
            print("=============")
            print(list_board)
        return render_template('board/board.html', name=user_info["name"], boards=list_board)
        # return redirect(url_for("", name=user_info["name"]))
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))



    # token_receive = request.cookies.get('mytoken')
    # try:
    #     payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    #     user_info = db.user.find_one({"id": payload['id']})
        
    #     comments = list(db.comment.find({}, {'_id': False}))
    #     for comment in comments:
    #         if comment['board_ojid'] == list_board['no']:
    #             list_board['comment'] = comment
        
    #     print("=============")
    #     print("=============")
    #     print(list_board)

        # comments_ojid = list(db.comment.find({}, {'_id': 0, 'co_user_id': 0, 'comment': 0, 'date': 0}))
        

        # test = []

        # for i in range(len(list_board)) :
        #     for j in range(len(comments)):
        #         if(list_board[i] == comments[j]):
        #             test.append(list_board[i] + comments[j])
                
        # for i in range(len(test)) : 
        #     print(test[i])


    #     return render_template('board/board.html', name=user_info["name"], boards=list_board, comments=comments)
    #     # return redirect(url_for("", name=user_info["name"]))
    # except jwt.ExpiredSignatureError:
    #     return redirect(url_for("login"))
    # except jwt.exceptions.DecodeError:
    #     return redirect(url_for("login"))


@app.route('/login')
def login():
    return render_template('main.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


#################################
##  로그인을 위한 API            ##
#################################

@app.route('/api/signup', methods=['POST'])
def api_signup_post() :

    url_id = request.form['url_id']
    url_pw = request.form['url_pw']
    url_pw2 = request.form['url_pw2']
    url_name = request.form['url_name']

    article = {'id': url_id, 'pw': url_pw, 'name': url_name}
    result = db.user.find_one({'id': url_id})

    if result is not None:
        return jsonify({'result': 'fail', 'msg': '이미 존재하는 아이디 입니다.'})
    else:
        if url_pw != url_pw2:
            return jsonify({'result': 'fail2', 'msg2': '비밀번호가 같지 않습니다.'})
        else:
            db.user.insert_one(article)
            return jsonify({'result': 'success'})

# 실시간 아이디 확인
@app.route('/id_check', methods=['POST'])
def id_check() :
    url_id = request.form['url_id']
    id_list = list(db.user.find({},{'_id':0, }))

    id_list_len = len(id_list)
    
    for i in range(id_list_len):
        id_se = id_list[i]['id']
        if id_se == url_id:
            return jsonify({'result': 'success'})            
    return jsonify({'result': 'bb'})   

# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    result = db.user.find_one({'id': id_receive, 'pw': pw_receive})

    # 찾으면 JWT 토큰을 만들어 발급
    if result is not None:
        payload = {
            'id': id_receive,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면 
    else:	
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
@app.route('/api/name', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:     
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'name': userinfo['name']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

#pageRoad Board
@app.route('/createBoard')
def create_board_page():
    return render_template("board/createBoard.html")

#Create Board
@app.route('/board', methods=['POST'])
def create_board():
    title = request.form['title']
    content = request.form['content']
    category = request.form['category']
    
    # 토큰을 가져오기
    token_receive = request.cookies.get('mytoken')
    
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        user_id = userinfo['name'] 
        db.boards.insert_one({'user_id':user_id, 'title':title, 'content':content, 'category':category, 'like': 0, 'date':time.strftime('%Y-%m-%d %X', time.localtime(time.time())) })
        return jsonify({'result': 'success'})
    
    #토큰 decode에 실패할때!
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '디코드 실패'})

## 댓글 등록
@app.route('/api/comment', methods=['POST'])
def api_comment():
    comment_form = request.form['comment']
    comment_ojid = request.form['ojid']
    token_receive = request.cookies.get('mytoken')

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        user_id = userinfo['id']
        db.comment.insert_one({
            'co_user_id': user_id, 
            'comment': comment_form, 
            'board_ojid': comment_ojid,
            'date':time.strftime('%Y-%m-%d %X', time.localtime(time.time()))})

        return jsonify({'result': 'success'})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


# user가 작성한 board list 찾기
@app.route('/api/board', methods=['GET'])
def user_board():
    token_receive = request.cookies.get('mytoken')
    
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        user_id = userinfo['name'] 
        
        boards = list(db.boards.find({'user_id' : user_id}))
        user_board = []
        
        for i in range(len(boards)):
            user_board.append(str(boards[i]['_id']))
            print(user_board[i])
        
        return jsonify({'result': 'success', 'user_board': user_board})
        
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '디코드 실패'})

@app.route('/api/<category>')
def category(category):
    #print(category)
    same_category = list(db.boards.find({'category':category}))
    for sc in same_category :
        print(sc)
    return redirect(url_for("home"))
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)