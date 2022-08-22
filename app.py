from flask import Flask
from flask import request
import sqlite3





app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_data(querry):
    conn = sqlite3.connect('Exchanger.sqlite3')
    conn.row_factory = dict_factory
    cursor = conn.execute(querry)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

# homepage
@app.route("/")
def Homepage():
    return "<p>Hello! This is the homepage</p>"


@app.route('/currency/list', methods = ['GET'])
def Currency_List():
    res = get_data(f"select * from Currency") # Виклик інфи
    return res

# 1page
@app.route('/currency/rating', methods=['GET', 'DELETE', 'POST', 'PUT'])
def Currency_review():
    if request.method == 'GET':
        res = get_data(f"select round(avg(Rating), 1), CurrencyName from Review GROUP by CurrencyName") #Виклик інфи
        return res
    else:
        pass

# 2page
@app.route('/currency/<currency_name>', methods = ['GET'])
def currency_info(currency_name):
    res = get_data(f"select * from Currency where Name ='{currency_name}'")
    return res

# 3page
@app.route('/currency/trade/<currency_name1>X<currency_name2>', methods = ['GET', 'POST'])
def trade_pair(currency_name1, currency_name2):
    if request.method == 'GET':
        res = get_data(f"""SELECT round((SELECT NameToUSDPrice from Currency WHERE Date = '12/08/2022' and Name = '{currency_name1}')/
        (SELECT NameToUSDPrice from Currency WHERE Date = '12/08/2022' and Name = '{currency_name2}'), 2)""")# Виклик інфи
        return res
    else:
        pass

# 5page
@app.route('/user/<id>', methods = ['GET'])
def User_Info(id):
    res = get_data(f"select * from User where id = '{id}'") # Виклик інфи
    return res


@app.post('/currency/<currency_name>/rating')
def add_currency_rating(currency_name):
    request_data = request.get_json()
    rating = request_data['Rating']
    comment = request_data['Comment']
    res = get_data(f"insert into Review (CurrencyName, Rating, Comment) values ('{currency_name}', '{rating}', '{comment}')")
    return res

@app.post('/currency/trade/<currency_name1>x<currency_name2>')
def exchange(currency_name1, currency_name2):
    request_data = request.get_json()
    user_id = 1
    amount1 = request_data['amount']
    date_time = request_data['datetime']
    OperType = request_data['OperType']
    fee = request_data['fee']

    user_balance1 = get_data(f"""select balance from Account where User_id = '{user_id}' and CurrencyName = '{currency_name1}' """)
    user_balance2 = get_data(f"""select balance from Account where User_id = '{user_id}' and CurrencyName = '{currency_name2}' """)
    act_currency1 = get_data(f"select * from Currency where CurrencyName = '{currency_name1}' ORDER BY Date DESC limit 1")
    curr1_cost_to_usd = act_currency1[0]['NameToUSDPrice']
    act_currency2 = get_data(f"select * from Currency where CurrencyName = '{currency_name2}' ORDER BY Date DESC limit 1")
    curr2_cost_to_usd = act_currency2[0]['NameToUSDPrice']

    needed_exchanger_balance = amount1 * curr1_cost_to_usd / curr2_cost_to_usd

    exchanger_balance = act_currency2[0]['Amount']

    if (user_balance1[0]['balance'] >= amount1) and (exchanger_balance >= needed_exchanger_balance):
        get_data(f"UPDATE Currency set Amount = {exchanger_balance - needed_exchanger_balance} where date = {act_currency2[0]['Date']} and CurrencyName = '{currency_name2}'")
        get_data(f"UPDATE Currency set Amount = {act_currency1[0]['Amount'] + amount1} where date = {act_currency2[0]['Date']} and CurrencyName = '{currency_name1}'")
        get_data(f"UPDATE Account set balance = {user_balance1[0]['balance']  -  amount1} where User_id = {user_id} and Currencyname = '{currency_name1}'")
        get_data(f"UPDATE Account set balance = {user_balance2[0]['balance'] + needed_exchanger_balance} where User_id = {user_id} and Currencyname = '{currency_name2}'")

        get_data(f"""INSERT into Transac
                (User,      OperationType, AmountofGivenCurrency, CurrencyTypeofGivingOper, CurrencyTypeofRecievingOper,      DateTime,    AmountofRecievedCurrency,     Fee, BalanceofGivingOper, BalanceofRecievingOper)values 
                ('{user_id}','{OperType}','    {amount1}',          '{currency_name1}',          '{currency_name2}',      '{date_time}',' {needed_exchanger_balance}', '{fee}', '{user_balance1}',   '{user_balance2}' )""")
        return 'ok'
    else:
        return 'not ok'

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

