from flask import Flask
from flask import request

app = Flask(__name__)


# homepage
@app.route("/")
def Homepage():
    return "<p>Hello! This is the homepage</p>"


# 1page
@app.route('/currency/<currency_name>/review', methods=['GET', 'DELETE', 'POST', 'PUT'])
def Currency_Review():
    return "<p>Here will be currency`s review</p>"


# 2page
@app.route('/currency/<currency_name>', methods = ['GET'])
def Currency_Page():
   return "<p>Here will be currency page including info, price, etc.</p>"

# 3page
@app.route('/currency/trade/<currency_name1>X<currency_name2>', methods = ['GET', 'POST'])
def Trade_Pair():
    return "<p>Here will be the info about the trading pair, and the ability to make an offer</p>"


# 4page
@app.route('/currency', methods = ['GET'])
def Coin_List():
    return "<p>Here will be list of all currencies and info about them(Trending, Price, Capitalisation)</p>"

# 5page
@app.route('/user', methods = ['GET'])
def User_Info():
    return "<p>Here will be info about user that currently logged in</p>"

# 6page
@app.route('/user/transfer', methods = ['POST'])
def Transfer_Operation():
    return "<p>Here will be page for performing transfer operations</p>"

@app.route('/user/history', methods = ['GET'])
def User_History_Page():
    return "<p>Here will be page representing history of user activities including deposits offers transfers etc.</p>"

@app.route('/user/deposit', methods = ['GET', 'POST'])
def Deposit_Page():
    return "<p>Here will be page with ability to deposit money </p>"

@app.route('/user/deposit/<deposit_id>', methods = ['GET'])
def Current_Deposit():
    return "<p>Here will be page showing info about certain deposit</p>"

@app.route('/deposit/<currency_name>', methods = ['POST'])
def MakeA_Deposit():
    return "<p>Here will be page performing an operation of deposit in certain currency</p>"
