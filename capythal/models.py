from datetime import datetime
from capythal import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))

class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    account = db.relationship("account", backref="user", lazy=True)

    def __repr__(self):
        return f"User('{self.email}', '{self.name}', '{self.surname}')"

class currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    account = db.relationship("account", backref="currency", lazy=True)

    def __repr__(self):
        return f"Currency('{self.name}')"

class card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    account = db.relationship("account", backref="card", lazy=True)

    def __repr__(self):
        return f"Card type('{self.id}', '{self.name}')"

class acc_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    account = db.relationship("account", backref="acc_type", lazy=True)

    def __repr__(self):
        return f"Account Type('{self.name}')"

class tr_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)

    category = db.relationship("category", backref="tr_type", lazy=True)
    transaction = db.relationship("transaction", backref="tr_type", lazy=True)

    def __repr__(self):
        return f"Transaction Type('{self.name}')"

class style(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    name_pl = db.Column(db.String(20), nullable=False)

    category = db.relationship("category", backref="style", lazy=True)
    account = db.relationship("account", backref="style", lazy=True)
    goal = db.relationship("goal", backref="style", lazy=True)

    def __repr__(self):
        return f"Style color('{self.name}')"

class category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'), nullable=False)
    tr_type_id = db.Column(db.Integer, db.ForeignKey('tr_type.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    icon = db.Column(db.String(20), nullable=False)

    transaction = db.relationship("transaction", backref="category", lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"

class account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    acc_type_id = db.Column(db.Integer, db.ForeignKey('acc_type.id'), nullable=False)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'), nullable=False)
    
    amount = db.Column(db.Float(20,2), default = 0)
    card_number = db.Column(db.String(4))
    fin_inst = db.Column(db.String(20))

    transaction = db.relationship("transaction", backref="account", lazy=True)
    goal = db.relationship("goal", backref="account", lazy=True)

    def __repr__(self):
        return f"Account('{self.id}')"

class transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    tr_type_id = db.Column(db.Integer, db.ForeignKey('tr_type.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(12,2), nullable=False)
    date = db.Column(db.Date, nullable=False , default=datetime.today)
    time = db.Column(db.Time, nullable=False , default=datetime.now().time())

    def __repr__(self):
        return f"Transaction('{self.name}', '{self.tr_type_id}', '{self.amount}', '{self.date}')"

class goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    style_id = db.Column(db.Integer, db.ForeignKey('style.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    amount_req = db.Column(db.Numeric(12,2), nullable=False)
    amount_avb = db.Column(db.Numeric(12,2), nullable=False)

    def __repr__(self):
        return f"Goal('{self.id}', '{self.style_id}', '{self.name}', '{self.amount_req}', '{self.amount_avb}')"
