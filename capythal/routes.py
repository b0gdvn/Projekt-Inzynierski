from flask import render_template, flash, url_for, redirect
from capythal import app, db, bcrypt
from capythal.forms import registrationForm, loginForm
from capythal.models import user, currency, card, fin_inst, acc_type, tr_type, style, category, account, transaction, settings, goal
from flask_login import login_user, logout_user, current_user

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
    
@app.route('/accounts')
def accounts():
    if current_user.is_authenticated:
        return render_template("accounts.html")
    else:
        return redirect(url_for('login'))
    

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