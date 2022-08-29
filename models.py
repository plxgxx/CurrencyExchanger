from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'
    login = db.Column(db.String(50), nullable = False)
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return '<User %r>' %self.login
    def to_dict(self):
        return {
            'login': self.login,
            'id': self.id,
            'password': self.password
        }

class Transac(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    User = db.Column(db.String(50), nullable = False)
    OperationType = db.Column(db.String(20), nullable = False)
    AmountofGivenCurrency = db.Column(db.REAL, nullable = False)
    CurrencyTypeofGivingOper = db.Column(db.String(50), nullable = False)
    CurrencyTypeofRecievingOper = db.Column(db.String(50), nullable = False)
    DateTime = db.Column(db.String(10), nullable = False)
    AmountofRecievedCurrency = db.Column(db.REAL, nullable=False)
    Fee = db.Column(db.REAL, nullable=False)
    BalanceofGivingOper = db.Column(db.Integer, nullable=False)
    BalanceofRecievingOper = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Transac %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'User': self.User,
            'OperationType': self.OperationType,
            'AmountofGivenCurrency': self.AmountofGivenCurrency,
            'CurrencyTypeofGivingOper': self.CurrencyTypeofGivingOper,
            'CurrencyTypeofRecievingOper': self.CurrencyTypeofRecievingOper,
            'DateTime': self.DateTime,
            'AmountofRecievedCurrency': self.AmountofRecievedCurrency,
            'Fee': self.Fee,
            'BalanceofGivingOper': self.BalanceofGivingOper,
            'BalanceofRecievingOper': self.BalanceofRecievingOper
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    CurrencyName = db.Column(db.String(20), nullable = False)
    Rating = db.Column(db.REAL,nullable = False)
    Comment = db.Column(db.String(100))

    def __repr__(self):
        return '<Review %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'CurrencyName': self.CurrencyName,
            'Rating': self.Rating,
            'Comment': self.Comment
        }

class Deposit(db.Model):
    DateofOpening = db.Column(db.String(10), nullable = False)
    DateofClosing = db.Column(db.String(10))
    DepositBalance = db.Column(db.Integer,nullable = False)
    InterestRate = db.Column(db.REAL, nullable = False)
    TermsofDeposit = db.Column(db.String, nullable = False)
    id = db.Column(db.String, primary_key=True, nullable = False)
    def __repr__(self):
        return '<Deposit %r>' % self.id


    def to_dict(self):
        return {
            'DateofOpening': self.DateofOpening,
            'DateofClosing': self.DateofClosing,
            'DepositBalance': self.DepositBalance,
            'InterestRate': self.InterestRate,
            'TermsofDeposit': self.TermsofDeposit,
            'id': self.id
        }

class Currency(db.Model):
    CurrencyName = db.Column(db.String(15),nullable = False)
    NameToUSDPrice = db.Column(db.REAL,nullable = False)
    Amount  = db.Column(db.REAL, nullable = False)
    Date = db.Column(db.String(10), nullable = False)
    id = db.Column(db.Integer, primary_key = True, nullable = False)

    def __repr__(self):
        return '<Currency %r>' % self.CurrencyName

    def to_dict(self):
        return {
            'CurrencyName': self.CurrencyName,
            'NameToUSDPrice': self.CurrencyName,
            'Amount': self.Amount,
            'Date': self.Date
        }
class Account(db.Model):
    User_id = db.Column(db.Integer, nullable = False)
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    balance = db.Column(db.REAL, nullable = False)
    CurrencyName = db.Column(db.String(15), nullable = False)

    def __repr__(self):
        return '<Account %r>' % self.id

    def to_dict(self):
        return {
            'User_id': self.User_id,
            'id': self.id,
            'balance': self.balance,
            'CurrencyName': self.CurrencyName
        }