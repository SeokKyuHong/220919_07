from crypt import methods
from turtle import title
from flask import Flask, render_template
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.project_02
collections = db.project_02

app = Flask(__name__)

@app.route('/signup', methods=['GET'])
def signup_read() :
    return render_template("signup.html")

@app.route('/signup', methods=['POST'])
def signup_post() :
    return render_template("signup.html")





if __name__ == '__main__':
   app.run('0.0.0.0',port=5001,debug=True)