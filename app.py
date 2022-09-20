from crypt import methods
from turtle import title
from flask import Flask, render_template
from pymongo import MongoClient
import datetime as dt
import time

client = MongoClient('mongodb://SecondWind:clsgowlrlfqkfo@13.125.11.60', 27017)
db = client.db_00_07

app = Flask(__name__)

@app.route('/signup', methods=['GET'])
def signup_read() :
    return render_template("signup.html")


@app.route('/signup', methods=['POST'])
def signup_post() :
    return render_template("signup.html")


#Read Board
@app.route('/board', methods=['GET'])
def read_board():
    boards = list(db.boards.find({},{'_id':False}))
    return render_template("board/board.html", boards=boards)


#Create Board
@app.route('/createBoard', methods=['GET'])
def create_board():
    
    
    return render_template("board/createBoard.html")


if __name__ == '__main__':
    app.run('0.0.0.0',port=4000,debug=True)