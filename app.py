
from os import lseek
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://SecondWind:clsgowlrlfqkfo@13.125.11.60', 27017)
db = client.db_00_07

app = Flask(__name__)

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
    return jsonify({'result': 'success'})

    # id_list = list(db.user.find({},{'_id':0, }))
    # id_list2 = db.user.find_one({'id': ''})
    # print(id_list)
    # id_list_len = len(id_list)
    # print(id_list_len)

# 회원가입 성공하면 로그인 페이지로 보내줌
@app.route('/index', methods=['GET'])
def main_read() :
    return render_template("index.html")

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
        
            
    
    




if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)