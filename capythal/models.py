from datetime import datetime
from capythal import db


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    settings = db.relationship("settings", back_populates="user", uselist=False)
    account = db.relationship("account", backref="user", lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.name}', '{self.surname}')"

class currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    account = db.relationship("account", backref="currency", lazy=True)
    settings = db.relationship("settings", backref="currency", lazy=True)

    def __repr__(self):
        return f"Currency('{self.name}')"

class card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    number = db.Column(db.Integer)

    account = db.relationship("account", backref="card", lazy=True)

    def __repr__(self):
        return f"Card type('{self.name}', '{self.number}')"

class fin_inst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

    account = db.relationship("account", backref="fin_inst", lazy=True)

    def __repr__(self):
        return f"Financial Institution('{self.name}')"

class acc_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    account = db.relationship("account", backref="acc_type", lazy=True)

    def __repr__(self):
        return f"Account Type('{self.name}')"

class tr_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    transaction = db.relationship("transaction", backref="tr_type", lazy=True)

    def __repr__(self):
        return f"Transaction Type('{self.name}')"

class style(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    category = db.relationship("category", backref="style", lazy=True)
    account = db.relationship("account", backref="style", lazy=True)
    goal = db.relationship("goal", backref="style", lazy=True)

    def __repr__(self):
        return f"Style color('{self.name}')"

class category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)

    transaction = db.relationship("transaction", backref="category", lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"

class account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    fin_inst_id = db.Column(db.Integer, db.ForeignKey('fin_inst.id'), nullable=False)
    acc_type_id = db.Column(db.Integer, db.ForeignKey('acc_type.id'), nullable=False)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'), nullable=False)

    transaction = db.relationship("transaction", backref="account", lazy=True)
    settings = db.relationship("settings", back_populates="account", uselist=False)
    goal = db.relationship("goal", backref="account", lazy=True)

    def __repr__(self):
        return f"Account('{self.id}')"

class transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    tr_type_id = db.Column(db.Integer, db.ForeignKey('tr_type.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False , default=datetime.utcnow)

    def __repr__(self):
        return f"Transaction('{self.title}', '{self.type}', '{self.amount}', '{self.datetime}')"

class settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)

    user = db.relationship("user", back_populates="settings") # used for one-one relationship
    account = db.relationship("account", back_populates="settings")

    def __repr__(self):
        return f"Settings('{self.id}', '{self.user_id}', '{self.account_id}', '{self.currency_id}')"

class goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    amount_req = db.Column(db.Numeric(12,2), nullable=False)
    amount_avb = db.Column(db.Numeric(12,2), nullable=False)

    def __repr__(self):
        return f"Goal('{self.id}', '{self.style_id}', '{self.title}', '{self.amount_req}', '{self.amount_avb}')"
