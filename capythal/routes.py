from flask import render_template, flash, url_for, redirect, request
from capythal import app, db, bcrypt, cache
from capythal.forms import registrationForm, loginForm, addAccForm, editAccForm, addGoalForm, editGoalForm, addIncTrForm, addExpTrForm, addTrfTrForm, editTrForm
from capythal.models import user, currency, card, acc_type, tr_type, style, category, account, transaction, goal
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import update, delete, desc
from random import randint
import datetime
from forex_python.converter import CurrencyRates
from forex_python.bitcoin import BtcConverter


# Kursy walut
cr = CurrencyRates()
bt = BtcConverter()

@cache.cached(timeout=3600, key_prefix='usd')
def usd_rate():
    try:
        return cr.get_rate('USD', 'PLN')
    except:
        return 4.5

@cache.cached(timeout=3600, key_prefix='eur')
def eur_rate():
    try:
        return cr.get_rate('EUR', 'PLN')
    except:
        return 4.7
    
@cache.cached(timeout=3600, key_prefix='gbp')
def gbp_rate():
    try:
        return cr.get_rate('GBP', 'PLN')
    except:
        return 5.4

@cache.cached(timeout=3600, key_prefix='btc')
def btc_rate():
    try:
        return bt.get_latest_price('PLN')
    except:
        return 74000

# Formatowanie wartości pieniędzy do postaci 0,000,000.00 PLN
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "{:,.2f}".format(value)

# Układ strony
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)

    accounts = db.session.query(account,currency,card,acc_type,style).join(currency).join(card).join(acc_type).join(style).filter(account.user_id == current_user.id)
    acc_types = db.session.query(acc_type).join(account).filter(account.user_id == current_user.id)
    acc_list = db.session.query(account).join(acc_type).filter(account.user_id == current_user.id)
    transactions = db.session.query(transaction,tr_type,account,currency)\
        .join(tr_type, transaction.tr_type_id==tr_type.id)\
        .join(account, transaction.account_id==account.id)\
        .join(currency, currency.id==account.currency_id)\
        .filter(account.user_id == current_user.id)
    transactions_last_week = db.session.query(transaction,tr_type,account,currency)\
        .join(tr_type, transaction.tr_type_id==tr_type.id)\
        .join(account, transaction.account_id==account.id)\
        .join(currency, currency.id==account.currency_id)\
        .filter(account.user_id == current_user.id)\
        .filter(transaction.date >= week_ago)
    
    amount_sum_last_week = 0
    for tr,type,acc,cur in transactions_last_week:
        if type.name == 'Wydatek':
            amount = float(-1 * tr.amount)
        else:
            amount = float(tr.amount)

        if cur.name == 'PLN':
            amount_sum_last_week = float(amount_sum_last_week) + amount
        elif cur.name == 'USD':
            amount_sum_last_week = float(amount_sum_last_week) + amount * usd_rate()
        elif cur.name == 'EUR':
            amount_sum_last_week = float(amount_sum_last_week) + amount * eur_rate()
        elif cur.name == 'GBP':
            amount_sum_last_week = float(amount_sum_last_week) + amount * gbp_rate()
        elif cur.name == 'BTC':
            amount_sum_last_week = float(amount_sum_last_week) + amount * btc_rate()

    amount_sum = 0
    for acc,cur,_,_,_ in accounts:
        if cur.name == 'PLN':
            amount_sum = float(amount_sum) + float(acc.amount)
        elif cur.name == 'USD':
            amount_sum = float(amount_sum) + float(acc.amount) * usd_rate()
        elif cur.name == 'EUR':
            amount_sum = float(amount_sum) + float(acc.amount) * eur_rate()
        elif cur.name == 'GBP':
            amount_sum = float(amount_sum) + float(acc.amount) * gbp_rate()
        elif cur.name == 'BTC':
            amount_sum = float(amount_sum) + float(acc.amount) * btc_rate()
    
    try:
        amount_chg = round((amount_sum + amount_sum_last_week) / amount_sum * 100) - 100
    except:
        amount_chg = 0

    income_sum_last_week = 0
    for tr,type,acc,cur in transactions_last_week:
        if type.name == 'Przychód':
            amount = float(tr.amount)

            if cur.name == 'PLN':
                income_sum_last_week = float(income_sum_last_week) + amount
            elif cur.name == 'USD':
                income_sum_last_week = float(income_sum_last_week) + amount * usd_rate()
            elif cur.name == 'EUR':
                income_sum_last_week = float(income_sum_last_week) + amount * eur_rate()
            elif cur.name == 'GBP':
                income_sum_last_week = float(income_sum_last_week) + amount * gbp_rate()
            elif cur.name == 'BTC':
                income_sum_last_week = float(income_sum_last_week) + amount * btc_rate()

    income_sum = 0
    for tr,type,acc,cur in transactions:
        if type.name == 'Przychód':
            amount = float(tr.amount)

            if cur.name == 'PLN':
                income_sum = float(income_sum) + amount
            elif cur.name == 'USD':
                income_sum = float(income_sum) + amount * usd_rate()
            elif cur.name == 'EUR':
                income_sum = float(income_sum) + amount * eur_rate()
            elif cur.name == 'GBP':
                income_sum = float(income_sum) + amount * gbp_rate()
            elif cur.name == 'BTC':
                income_sum = float(income_sum) + amount * btc_rate()
    
    try:
        income_chg = round((income_sum + income_sum_last_week) / income_sum * 100) - 100
    except:
        income_chg = 0

    expense_sum_last_week = 0
    for tr,type,acc,cur in transactions_last_week:
        if type.name == 'Wydatek':
            amount = float(tr.amount)

            if cur.name == 'PLN':
                expense_sum_last_week = float(expense_sum_last_week) + amount
            elif cur.name == 'USD':
                expense_sum_last_week = float(expense_sum_last_week) + amount * usd_rate()
            elif cur.name == 'EUR':
                expense_sum_last_week = float(expense_sum_last_week) + amount * eur_rate()
            elif cur.name == 'GBP':
                expense_sum_last_week = float(expense_sum_last_week) + amount * gbp_rate()
            elif cur.name == 'BTC':
                expense_sum_last_week = float(expense_sum_last_week) + amount * btc_rate()

    expense_sum = 0
    for tr,type,acc,cur in transactions:
        if type.name == 'Wydatek':
            amount = float(tr.amount)

            if cur.name == 'PLN':
                expense_sum = float(expense_sum) + amount
            elif cur.name == 'USD':
                expense_sum = float(expense_sum) + amount * usd_rate()
            elif cur.name == 'EUR':
                expense_sum = float(expense_sum) + amount * eur_rate()
            elif cur.name == 'GBP':
                expense_sum = float(expense_sum) + amount * gbp_rate()
            elif cur.name == 'BTC':
                expense_sum = float(expense_sum) + amount * btc_rate()
    
    try:
        expense_chg = round((expense_sum + expense_sum_last_week) / expense_sum * 100) - 100
    except:
        expense_chg = 0
        
    return render_template("home.html", amount_sum = amount_sum, amount_chg = amount_chg, income_sum = income_sum, income_chg = income_chg, expense_sum = expense_sum, expense_chg = expense_chg,\
        accounts = accounts, acc_types = acc_types, acc_list = acc_list, pct = 30)
    
@app.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    form_add = addAccForm()
    form_edit = editAccForm()

    accounts = db.session.query(account,currency,card,acc_type,style).join(currency).join(card).join(acc_type).join(style).filter(account.user_id == current_user.id)
    
    if form_add.submitNewAcc.data and form_add.validate():
        new_acc = account(user_id = current_user.id, amount = form_add.amount.data, currency_id = form_add.currency.data, card_id = form_add.card_type.data, acc_type_id = form_add.acc_type.data,\
            style_id = randint(1,10), card_number = form_add.card_number.data, fin_inst = form_add.fin_inst.data )
        db.session.add(new_acc)
        db.session.commit()
        return redirect(url_for('accounts'))

    if form_edit.submitEditAcc.data and form_edit.validate():
        db.session.execute(
            update(account)
            .where((account.id == form_edit.account_id.data) & (account.user_id == current_user.id))
            .values(currency_id = form_edit.currency.data, card_id = form_edit.card_type.data, acc_type_id = form_edit.acc_type.data, card_number = form_edit.card_number.data, fin_inst = form_edit.fin_inst.data))

        db.session.commit()
        return redirect(url_for('accounts'))
    
    if form_edit.deleteAcc.data and form_edit.validate():
        db.session.execute(
            delete(account)
            .where((account.id == form_edit.account_id.data) & (account.user_id == current_user.id)))
        # when account is deleted, delete connected goals and transactions

        db.session.commit()
        return redirect(url_for('accounts'))

    return render_template("accounts.html", accounts = accounts, form_add = form_add, form_edit = form_edit)

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    form_add = addGoalForm()
    form_edit = editGoalForm()

    goals = db.session.query(goal,account,currency,style).join(account, goal.account_id==account.id).join(currency, currency.id==account.currency_id).join(style, goal.style_id==style.id)\
        .filter(account.user_id == current_user.id)
    
    user_accs = db.session.query(account,acc_type).join(acc_type).join(style).filter(account.user_id == current_user.id)
    accs_list = [(i.account.id, f"{i.account.fin_inst} - {i.acc_type.name}") for i in user_accs]
    form_add.account.choices = accs_list
    form_edit.account.choices = accs_list

    if form_add.submitNewGoal.data and form_add.validate():
        new_goal = goal(account_id = form_add.account.data, amount_req = form_add.amount_req.data, amount_avb = form_add.amount_avb.data, style_id = randint(1,10), name = form_add.name.data)
        db.session.add(new_goal)
        db.session.commit()
        return redirect(url_for('goals'))

    if form_edit.submitEditGoal.data:
        db.session.execute(
            update(goal)
            .where(goal.id == form_edit.goal_id.data)
            .values(account_id = form_add.account.data, amount_req = form_add.amount_req.data, amount_avb = form_add.amount_avb.data, name = form_add.name.data))

        db.session.commit()
        return redirect(url_for('goals'))
    
    if form_edit.deleteGoal.data:
        db.session.execute(
            delete(goal)
            .where((goal.id == form_edit.goal_id.data)))

        db.session.commit()
        return redirect(url_for('goals'))

    return render_template("goals.html", goals = goals, form_add = form_add, form_edit = form_edit, accs_list = accs_list)

@app.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    form_inc_add = addIncTrForm()
    form_exp_add = addExpTrForm()
    form_trf_add = addTrfTrForm()
    form_edit = editTrForm()

    page = request.args.get('page',1,type=int)
    transactions = db.session.query(transaction,tr_type,account,currency,category,style)\
        .join(tr_type, transaction.tr_type_id==tr_type.id)\
        .join(account, transaction.account_id==account.id)\
        .join(currency, currency.id==account.currency_id)\
        .join(category, transaction.category_id==category.id)\
        .join(style, category.style_id==style.id)\
        .filter(account.user_id == current_user.id)\
        .order_by(desc(transaction.date))\
        .paginate(page=page, per_page=5)
    
    tr_dates = []
    for tr_date in transactions.items:
        if not tr_date.transaction.date in tr_dates:
            tr_dates.append(tr_date.transaction.date)

    inc_cat_list = db.session.query(category).filter(category.tr_type_id == 2)
    form_inc_add.inc_category.choices = [(i.id, i.name) for i in inc_cat_list]

    exp_cat_list = db.session.query(category).filter(category.tr_type_id == 1)
    form_exp_add.exp_category.choices = [(i.id, i.name) for i in exp_cat_list]

    user_accs = db.session.query(account,acc_type,currency).join(acc_type).join(style).join(currency).filter(account.user_id == current_user.id)
    accs_list = [(i.account.id, f"{i.account.fin_inst} - {i.acc_type.name} {i.currency.name}") for i in user_accs]
    form_inc_add.account.choices = accs_list
    form_exp_add.account.choices = accs_list
    form_trf_add.account_f.choices = accs_list
    form_trf_add.account_to.choices = accs_list

    if form_inc_add.submitNewTr.data and form_inc_add.validate():
        acc = db.session.query(account).where(account.id == form_inc_add.account.data).first()
        
        new_tr = transaction(account_id = form_inc_add.account.data, category_id = form_inc_add.inc_category.data, tr_type_id = form_inc_add.tr_type_id.data,\
            name = form_inc_add.tr_name.data, amount = form_inc_add.tr_amount.data, date = form_inc_add.tr_date.data, time = form_inc_add.tr_time.data)
        db.session.add(new_tr)

        db.session.execute(
            update(account)
            .where(account.id == form_exp_add.account.data)
            .values(amount = (float(acc.amount) + float(form_inc_add.tr_amount.data))))

        db.session.commit()
        return redirect(url_for('history'))
    
    if form_exp_add.submitNewTr.data and form_exp_add.validate():
        acc = db.session.query(account).where(account.id == form_exp_add.account.data).first()

        new_tr = transaction(account_id = form_exp_add.account.data, category_id = form_exp_add.exp_category.data, tr_type_id = form_exp_add.tr_type_id.data,\
            name = form_exp_add.tr_name.data, amount = form_exp_add.tr_amount.data, date = form_exp_add.tr_date.data, time = form_exp_add.tr_time.data)
        db.session.add(new_tr)

        db.session.execute(
            update(account)
            .where(account.id == form_exp_add.account.data)
            .values(amount = (float(acc.amount) - float(form_exp_add.tr_amount.data))))

        db.session.commit()
        return redirect(url_for('history'))

    if form_trf_add.submitNewTr.data and form_trf_add.validate():
        acc_f,acc_f_cur = db.session.query(account,currency).join(currency).where(account.id == form_trf_add.account_f.data).first()
        cur_f = acc_f_cur.name
        acc_to,acc_to_cur = db.session.query(account,currency).join(currency).where(account.id == form_trf_add.account_to.data).first()
        cur_to = acc_to_cur.name

        if cur_f == cur_to:
            amount_to = form_trf_add.tr_amount.data
        elif cur_f == 'BTC':
            amount_to = round(bt.convert_btc_to_cur(form_trf_add.tr_amount.data, cur_to),2)
        elif cur_to == 'BTC':
            amount_to = round(bt.convert_to_btc(form_trf_add.tr_amount.data, cur_f),2)
        else:
            amount_to = round(cr.convert(cur_f, cur_to, form_trf_add.tr_amount.data),2)
        
        new_tr_f = transaction(account_id = form_trf_add.account_f.data, category_id = 19, tr_type_id = 1, name = f'Transfer - Wpływ',\
            amount = form_trf_add.tr_amount.data, date = form_trf_add.tr_date.data, time = form_trf_add.tr_time.data)
        new_tr_to = transaction(account_id = form_trf_add.account_to.data, category_id = 19, tr_type_id = 2, name = f'Transfer - Wychodzący',\
            amount = amount_to, date = form_trf_add.tr_date.data, time = form_trf_add.tr_time.data)
        db.session.add(new_tr_to)
        db.session.add(new_tr_f)

        db.session.execute(
            update(account)
            .where(account.id == form_trf_add.account_f.data)
            .values(amount = (float(acc_f.amount) - form_trf_add.tr_amount.data)))
            
        db.session.execute(
            update(account)
            .where(account.id == form_trf_add.account_to.data)
            .values(amount = (float(acc_to.amount) + amount_to)))

        db.session.commit()
        return redirect(url_for('history'))

    if form_edit.submitEditTr.data:
        acc = db.session.query(account).where(account.id == form_edit.tr_acc.data).first()
        tr = db.session.query(transaction).where(transaction.id == form_edit.tr_id.data).first()
        tr_amount_before = tr.amount
        
        db.session.execute(
            update(transaction)
            .where(transaction.id == form_edit.tr_id.data)
            .values(name = form_edit.tr_name.data, amount = form_edit.tr_amount.data, date = form_edit.tr_date.data, time = form_edit.tr_time.data))
        
        if 'Przychód' in str(tr.tr_type):
            db.session.execute(
                update(account)
                .where(account.id == form_edit.tr_acc.data)
                .values(amount = (float(acc.amount) - float(tr_amount_before) + float(form_edit.tr_amount.data))))

        elif 'Wydatek' in str(tr.tr_type):
            db.session.execute(
                update(account)
                .where(account.id == form_edit.tr_acc.data)
                .values(amount = (float(acc.amount) + float(tr_amount_before) - float(form_edit.tr_amount.data))))

        db.session.commit()
        return redirect(url_for('history'))
    
    if form_edit.deleteTr.data:
        acc = db.session.query(account).where(account.id == form_edit.tr_acc.data).first()
        tr = db.session.query(transaction).where(transaction.id == form_edit.tr_id.data).first()
        tr_amount_del = tr.amount

        db.session.execute(
            delete(transaction)
            .where(transaction.id == form_edit.tr_id.data))

        if 'Przychód' in str(tr.tr_type):
            db.session.execute(
                update(account)
                .where(account.id == form_edit.tr_acc.data)
                .values(amount = (float(acc.amount) - float(tr_amount_del))))

        elif 'Wydatek' in str(tr.tr_type):
            db.session.execute(
                update(account)
                .where(account.id == form_edit.tr_acc.data)
                .values(amount = (float(acc.amount) + float(tr_amount_del))))

        db.session.commit()
        return redirect(url_for('history'))

    return render_template("history.html", transactions = transactions, tr_dates = tr_dates, accs_list = accs_list, inc_cat_list = inc_cat_list, exp_cat_list = exp_cat_list, form_inc_add = form_inc_add, form_exp_add = form_exp_add, form_trf_add = form_trf_add, form_edit = form_edit)

@app.route('/userpage')
@login_required
def userpage():
    return render_template("userpage.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = registrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = user(name = form.user_name.data, surname = form.user_surname.data, email = form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash(f'Witaj {form.user_name.data}, twoje konto zostało utworzone!', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = loginForm()
    if form.validate_on_submit():
        user_login = user.query.filter_by(email=form.email.data).first()
        if user_login and bcrypt.check_password_hash(user_login.password, form.password.data):
            login_user(user_login, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Logowanie nie powiodło się, spróbuj ponownie', 'danger')
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))