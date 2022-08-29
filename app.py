import datetime
from flask import Flask
from flask import request
from sqlalchemy import func, create_engine
from sqlalchemy.orm import sessionmaker
import models
from models import db, User, Transac, Review, Deposit, Currency, Account


app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Exchanger.sqlite3'
db.init_app(app)
engine = create_engine('sqlite:///Exchanger.sqlite3')
Session = sessionmaker(bind = engine)
session = Session()
date_now = datetime.datetime.now().strftime("%d-%m-%Y")







# homepage
@app.route("/")
def Homepage():
    return "<p>Hello! This is the homepage</p>"


@app.route('/currency/list', methods=['GET'])#Works
def Currency_List():
    result = Currency.query.all()
    return [itm.to_dict() for itm in result]


# 2page
@app.route('/currency/<currency_name>', methods=['GET'])#Works
def currency_info(currency_name):
    res = Currency.query.filter_by(CurrencyName=currency_name)
    return [itm.to_dict() for itm in res]


# 3page
@app.get('/currency/trade/<currency_name1>X<currency_name2>')#Works
def trade_pair(currency_name1, currency_name2):
    res = round((Currency.query.filter_by(CurrencyName=currency_name1,
                                               Date=date_now).first().NameToUSDPrice) / (
                     Currency.query.filter_by(CurrencyName=currency_name2,
                                              Date=date_now).first().NameToUSDPrice), 2)
    return f"The cost of {currency_name1} to {currency_name2} : {res}"


# 5page
@app.route('/users', methods=['GET'])#works
def get_users():
    result = User.query.all()
    return [itm.to_dict() for itm in result]


@app.route('/currency/<currency_name>/rating', methods = ['GET', 'POST'])#works
def add_currency_rating(currency_name):
    if request.method == 'POST':
        request_data = request.get_json()
        rating = request_data['Rating']
        comment = request_data['Comment']
        rating_piece = Review(CurrencyName=currency_name, Rating=rating, Comment=comment)
        db.session.add(rating_piece)
        db.session.commit()
        return "ok!"
    else:
        all_ratings = Review.query.all()
        currency_rating = dict(db.session.querry(
            db.func.avg(models.Review.Rating).lable('rate').filter(models.Review.CurrencyName == currency_name)
        ).first())['rate']
        return f"Ratings of {currency_name}: {[itm.to_dict() for itm in all_ratings]}, average: {currency_rating}"


@app.post('/currency/trade/<currency_name1>x<currency_name2>')#Works
def exchange(currency_name1, currency_name2):
    request_data = request.get_json()
    user_id = request_data['user_id']
    amount1 = request_data['amount']
    OperType = request_data['OperType']
    fee = request_data['fee']

    user_balance1 = Account.query.filter_by(CurrencyName=currency_name1, User_id=user_id).first()
    act_currency1 = Currency.query.filter_by(CurrencyName=currency_name1, Date=date_now).first()
    act_currency2 = Currency.query.filter_by(CurrencyName=currency_name2, Date=date_now).first()

    needed_exchanger_balance = (amount1 * act_currency1.NameToUSDPrice / act_currency2.NameToUSDPrice)

    if act_currency2.Amount >= needed_exchanger_balance:
        if user_balance1.balance >= amount1:
            new_userbalance1 = user_balance1.balance - amount1
            Account.query.filter_by(User_id=user_id, CurrencyName=currency_name1).update(dict(balance=new_userbalance1))

            user_balance2 = Account.query.filter_by(CurrencyName=currency_name2, User_id=user_id).first()
            if user_balance2 is None:
                created_balance = Account(User_id=user_id, balance=needed_exchanger_balance,
                                          CurrencyName=currency_name2)
                db.session.add(created_balance)
            elif user_balance2 is not None:
                new_userbalance2 = user_balance2.balance + needed_exchanger_balance
                user_balance2.balance = new_userbalance2



            new_exchangerbalance2 = "{:.2f}".format(act_currency2.Amount - needed_exchanger_balance)
            act_currency2.Amount = new_exchangerbalance2

            new_exchangerbalance1 = act_currency1.Amount + amount1
            act_currency1.Amount = new_exchangerbalance1

            balance_value1 = user_balance1.balance
            balance_value2 = user_balance2.balance
            successfultransac = Transac(User=user_id, OperationType=OperType,
                                        AmountofGivenCurrency=amount1,
                                        CurrencyTypeofGivingOper=currency_name1,
                                        CurrencyTypeofRecievingOper=currency_name2,
                                        DateTime=date_now, AmountofRecievedCurrency=needed_exchanger_balance,
                                        Fee=fee, BalanceofGivingOper=balance_value1,
                                        BalanceofRecievingOper=balance_value2)
            db.session.add(successfultransac)
            db.session.commit()
            return "Successful transaction!"
        else:
            return "Not enough funds on user balance"
    else:
        return "Not enough funds in exchanger"




if __name__ == '__main__':
    app.run()
