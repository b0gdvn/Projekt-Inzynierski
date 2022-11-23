from flask import render_template, flash, url_for, redirect
from capythal import app, db, bcrypt
from capythal.forms import registrationForm, loginForm, addAccForm, editAccForm, addGoalForm, editGoalForm
from capythal.models import user, currency, card, acc_type, tr_type, style, category, account, transaction, settings, goal
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import update, delete
from random import randint

# Formatowanie wartości pieniędzy
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "{:,.2f}".format(value)

# Układ strony
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    accounts = db.session.query(account,currency,card,acc_type,style).join(currency).join(card).join(acc_type).join(style).filter(account.user_id == current_user.id)
    acc_types = db.session.query(acc_type).join(account).filter(account.user_id == current_user.id)
    acc_list = db.session.query(account).join(acc_type).filter(account.user_id == current_user.id)

    return render_template("home.html", accounts = accounts, acc_types = acc_types, acc_list = acc_list)

@app.route('/stats')
@login_required
def stats():
    return render_template("stats.html")
    
@app.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    form_add = addAccForm()
    form_edit = editAccForm()

    accounts = db.session.query(account,currency,card,acc_type,style).join(currency).join(card).join(acc_type).join(style).filter(account.user_id == current_user.id)
    
    if form_add.submitNewAcc.data and form_add.validate():
        new_acc = account(user_id = current_user.id, amount = form_add.amount.data, currency_id = form_add.currency.data, card_id = form_add.card_type.data, acc_type_id = form_add.acc_type.data, style_id = randint(1,10), card_number = form_add.card_number.data, fin_inst = form_add.fin_inst.data )
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

        db.session.commit()
        return redirect(url_for('accounts'))

    return render_template("accounts.html", accounts = accounts, form_add = form_add, form_edit = form_edit)

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    form_add = addGoalForm()
    form_edit = editGoalForm()

    goals = db.session.query(goal,account,currency,style).join(account, goal.account_id==account.id).join(currency, currency.id==account.currency_id).join(style, goal.style_id==style.id).filter(account.user_id == current_user.id)
    
    user_accs = db.session.query(account,acc_type).join(acc_type).join(style).filter(account.user_id == current_user.id)
    accs_list = [(i.account.id, f"{i.account.fin_inst} - {i.acc_type.name}") for i in user_accs]
    form_add.account.choices = accs_list
    form_edit.account.choices = accs_list

    if form_add.submitNewGoal.data and form_add.validate():
        new_goal = goal(account_id = form_add.account.data, amount_req = form_add.amount_req.data, amount_avb = form_add.amount_avb.data, style_id = randint(1,10), name = form_add.name.data )
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
    

@app.route('/history')
@login_required
def history():
    return render_template("history.html")

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