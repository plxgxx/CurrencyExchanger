from flask import Flask
from flask import request
import sqlite3





app = Flask(__name__)

def get_data(querry:str):
    conn = sqlite3.connect('Exchanger.sqlite3')
    cursor = conn.execute(querry)
    result = cursor.fetchall()
    conn.close()
    return result

# homepage
@app.route("/")
def Homepage():
    return "<p>Hello! This is the homepage</p>"

# 1page
@app.route('/currency', methods=['GET', 'DELETE', 'POST', 'PUT'])
def Currency_review():
    if request.method == 'GET':
        res = get_data(f"select round(avg(Rating), 1), CurrencyName from Review GROUP by CurrencyName")
        return res
    else:
        pass

# 2page
@app.route('/currency/<currency_name>', methods = ['GET'])
def currency_list(currency_name):
    res = get_data(f"select * from Currency where Name ='{currency_name}'")
    return res

# 3page
@app.route('/currency/trade/<currency_name1>X<currency_name2>', methods = ['GET', 'POST'])
def trade_pair(currency_name1, currency_name2):
    if request.method == 'GET':
        res = get_data(f"""SELECT round((SELECT NameToUSDPrice from Currency WHERE Date = '12/08/2022' and Name = '{currency_name1}')/
        (SELECT NameToUSDPrice from Currency WHERE Date = '12/08/2022' and Name = '{currency_name2}'), 2)""")
        return res
    else:
        pass

# 5page
@app.route('/user/<id>', methods = ['GET'])
def User_Info(id):
    res = get_data(f"select * from User where id = '{id}'")
    return res



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

