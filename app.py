from flask import Flask, render_template, jsonify, request, session, redirect, url_for

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
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        boards = list(db.boards.find({}, {'_id': False}))
        return render_template('board/board.html', name=user_info["name"], boards=boards)
        # return redirect(url_for("", name=user_info["name"]))
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


@app.route('/login')
def login():
    # msg = request.args.get("msg")
    return render_template('main.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


#################################
##  로그인을 위한 API            ##
#################################

# [회원가입 API]
# id, pw, nickname을 받아서, mongoDB에 저장
# 저장하기 전, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장

# 회원가입 데이터 전송, 아이디 중복 차단,
@app.route('/api/signup', methods=['POST'])
def api_signup_post() :

    url_id = request.form['url_id']
    url_pw = request.form['url_pw']
    url_pw2 = request.form['url_pw2']
    url_name = request.form['url_name']

    print(url_id)

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

# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 회원가입 때와 같은 방법으로 pw를 암호화
    # pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    # id, 암호화된pw을 가지고 해당 유저를 찾기
    result = db.user.find_one({'id': id_receive, 'pw': pw_receive})

    # 찾으면 JWT 토큰을 만들어 발급
    if result is not None:
        # JWT 토큰에는, payload와 시크릿키가 필요함
        # 시크릿키가 있어야 토큰을 디코딩(=풀기) 해서 payload 값을 볼 수 있음
        # 아래에선 id와 exp를 담음. 즉, JWT 토큰을 풀면 유저ID 값을 알 수 있음
        # exp는 만료시간. 시간이 지나면, 시크릿키로 토큰을 풀 때 만료되었다고 에러가 남
        payload = {
            'id': id_receive,
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        										# token을 줍니다.
        return jsonify({'result': 'success', 'token': token})
    else:	# 찾지 못하면
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/name', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'name': userinfo['name']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})

#Read Board
@app.route('/board', methods=['GET'])
def read_board():
    
    boards = db.boards.find({})
    
    list_board = list(db.boards.find({},{'_id':False}))

    for i in range(len(list_board)):
        id = str(boards[i]['_id'])
        list_board[i]['no'] = id
        print(list_board[i])

    #db.boards.insert_one({'user_id':'', 'title':'안녕', 'content':'전산학 사전지식이 없는 졸업생/직장인들을 대상으로, 5개월 간의 몰입 과정을 장기적으로 성장할 수 있는 정예 개발자를 길러내는 코스입니전산학과를 졸업하지 않았으면 개발자가 되기에 늦은 것일까요?훌륭한 개발자는 타고난 것일까요? 저희는 그렇게 생각하지 않습니다.문제를 깊수준까지 파고 들어갈 전산학 핵심 내용을 공부하고,어려운 실습 과정을 동료들과 끝까지 실행하는 훈련을 통해, 충분히 거듭날 수 있습니다.과제와 도전의 연속인 교육 과정은, 험난한 정글 같습니다.하지만 SW사관학교 정글을 수료한다면,이전과는 다른 미래를 그리는, 어디서든 탐내는인재로 거듭난 자신을 마주할 것입니다.정글에서 떠오르는 해를 보면서 보물을 찾는 경험. 함께 하시죠!', 'category':'잡담', 'like': 0, 'date':time.strftime('%Y-%m-%d %X', time.localtime(time.time())) })
    return render_template("board/board.html", boards=list_board)

#Create Board
@app.route('/createBoard', methods=['GET'])
def create_board():
    return render_template("board/createBoard.html")

## 댓글 등록
@app.route('/api/comment', methods=['POST'])
def api_comment():
    comment_form = request.form['comment']
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
        db.comment.insert_one({'co_user_id': user_id, 'comment': comment_form})

        return jsonify({'result': 'success'})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


## 댓글 리스트


if __name__ == '__main__':
    app.run('0.0.0.0', port=5005, debug=True)