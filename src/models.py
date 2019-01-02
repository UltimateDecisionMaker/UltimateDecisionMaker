from . import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from passlib.hash import sha256_crypt
from datetime import datetime as dt

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class History(db.Model):

    __tablename__ = 'histories'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.ForeignKey('accounts.id'), nullable=False)
    options = db.Column(db.String(128))

    user = db.relationship('Account', backref='history', lazy=True)



class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    histories = db.relationship('History', backref='account', lazy=True)

    date_created = db.Column(db.DateTime, default=dt.now())



    def __repr__(self):
        return '<Account {}>'.format(self.email)

    def __init__(self, email, password):
        self.email = email
        self.password = sha256_crypt.hash(password)

    @classmethod
    def check_password_hash(cls, account, password):
        if account:
            if sha256_crypt.verify(password, account.password):
                return True
        return False


