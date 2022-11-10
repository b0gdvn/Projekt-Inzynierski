from flask import Flask, render_template, flash, url_for, redirect
from forms import registrationForm, loginForm
import os

app=Flask(__name__)

# Klucz autentyfikacji
app.config['SECRET_KEY'] = 'd91fa1479fcdb3eaa587fd43f44ea668'

# Formatowanie wartości pieniędzy
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "{:,.2f}".format(value)



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

# Układ strony
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/stats')
def stats():
    return render_template("stats.html")
    
@app.route('/accounts')
def accounts():
    return render_template("accounts.html")

@app.route('/goals')
def goals():
    return render_template("goals.html", goals_list = goals_list)

@app.route('/history')
def history():
    return render_template("history.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registrationForm()
    if form.validate_on_submit():
        flash(f'Witaj {form.user_name.data}, twoje konto zostało utworzone!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

@app.route('/login')
def login():
    form = loginForm()
    return render_template("login.html", form=form)

# Uruchomienie aplikacji
if __name__=="__main__":
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 4444)))