from flask import render_template, flash, url_for, redirect
from capythal import app, db, bcrypt
from capythal.forms import registrationForm, loginForm, addAccForm, editAccForm, idForm
from capythal.models import user, currency, card, acc_type, tr_type, style, category, account, transaction, settings, goal
from flask_login import login_user, logout_user, current_user, login_required
from random import randint

# Dane
goals_list = [
    {
        'name': 'Wycieczka do Paryża',
        'amount_available': 2772.00,
        'amount_required': 3600.00,
        'currency': 'PLN',
        'percentage': 77,
        'color': 'orange'
    },
    {
        'name': 'Remont Mieszkania',
        'amount_available': 3000.00,
        'amount_required': 12000.00,
        'currency': 'PLN',
        'percentage': 25,
        'color': 'blue'
    },
    {
        'name': 'Zakup Samochodu',
        'amount_available': 23220.00,
        'amount_required': 43000.00,
        'currency': 'PLN',
        'percentage': 54,
        'color': 'green'
    }
]

# Formatowanie wartości pieniędzy
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "{:,.2f}".format(value)

# Układ strony
@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template("home.html")
    else:
        return redirect(url_for('login'))    

@app.route('/stats')
def stats():
    if current_user.is_authenticated:
        return render_template("stats.html")
    else:
        return redirect(url_for('login'))
    
@app.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    form_add = addAccForm()
    form_edit = editAccForm()
    form_id = idForm()

    i = 1
    accounts = db.session.query(account,currency,card,acc_type,style).join(currency).join(card).join(acc_type).join(style).filter(account.user_id == current_user.id)
    
    if form_add.validate_on_submit():
        new_acc = account(user_id = current_user.id, currency_id = form_add.currency.data, card_id = form_add.card_type.data, acc_type_id = form_add.acc_type.data, style_id = randint(1,10), card_number = form_add.card_number.data, fin_inst = form_add.fin_inst.data )
        db.session.add(new_acc)
        db.session.commit()
        return redirect(url_for('accounts'))
    
    
    # form_edit.card_number.data = form_id


    if form_edit.validate_on_submit():
        edit_acc = account(user_id = current_user.id, currency_id = form_add.currency.data, card_id = form_add.card_type.data, acc_type_id = form_add.acc_type.data, style_id = randint(1,10), card_number = form_add.card_number.data, fin_inst = form_add.fin_inst.data )
        db.session.add(edit_acc)
        db.session.commit()
        return redirect(url_for('accounts')) 

    return render_template("accounts.html", accounts = accounts, form_add = form_add, form_edit = form_edit, form_id = form_id)



@app.route('/goals')
def goals():
    if current_user.is_authenticated:
        return render_template("goals.html", goals_list = goals_list)
    else:
        return redirect(url_for('login'))
    

@app.route('/history')
def history():
    if current_user.is_authenticated:
        return render_template("history.html")
    else:
        return redirect(url_for('login'))

@app.route('/userpage')
def userpage():
    if current_user.is_authenticated:
        return render_template("userpage.html")
    else:
        return redirect(url_for('login'))


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