from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from capythal.models import user
from datetime import datetime, date

class registrationForm(FlaskForm):
    user_name = StringField('Imię', validators=[DataRequired(), Length(min=1, max=30)])
    user_surname = StringField('Nazwisko', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Powtórz Hasło', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Zarejestruj Się')

    def validate_email(self, email):
        email = user.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError('Konto użytkownika ze wskazaną pocztą już istnieje, spróbuj się zalogować')

class loginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj Się')

class addAccForm(FlaskForm):
    amount = FloatField('Aktualne saldo')
    currency = SelectField('Waluta',[DataRequired()],choices=[(1, 'PLN'), (2, 'USD'), (3, 'EUR'), (4, 'GBP'), (5, 'BTC')])
    card_type = SelectField('Karta',[DataRequired()],choices=[(1, '-'), (2, 'MasterCard' ), (3, 'Visa'), (4, 'Inna')])
    acc_type = SelectField('Typ Konta',[DataRequired()],choices=[(1, 'Rachunek Bieżący'), (2, 'Karta Kredytowa'), (3, 'Konto Maklerskie'), (4, 'Gotówka'), (5, 'Inne')])
    card_number = StringField('Ostatnie 4 cyfry Karty', validators=[Length(max=4)], render_kw={'placeholder': 'Ostatnie 4 cyfry karty'})
    fin_inst = StringField('Instytucja Finansowa', validators=[Length(max=20)], render_kw={'placeholder': 'Nazwa Instytucji Finansowej'})
    submitNewAcc = SubmitField('Dodaj')

class editAccForm(FlaskForm):
    currency = SelectField('Waluta',[DataRequired()],choices=[(1, 'PLN'), (2, 'USD'), (3, 'EUR'), (4, 'GBP'), (5, 'BTC')])
    card_type = SelectField('Karta',[DataRequired()],choices=[(1, '-'), (2, 'MasterCard' ), (3, 'Visa'), (4, 'Inna')])
    acc_type = SelectField('Typ Konta',[DataRequired()],choices=[(1, 'Rachunek Bieżący'), (2, 'Karta Kredytowa'), (3, 'Konto Maklerskie'), (4, 'Gotówka'), (5, 'Inne')])
    card_number = StringField('Ostatnie 4 cyfry Karty', validators=[Length(max=4)], render_kw={'placeholder': 'Ostatnie 4 cyfry karty'})
    fin_inst = StringField('Instytucja Finansowa', validators=[Length(max=20)], render_kw={'placeholder': 'Nazwa Instytucji Finansowej'})
    account_id = StringField('account_id')
    submitEditAcc = SubmitField('Zapisz')
    deleteAcc = SubmitField('Usuń')

class addGoalForm(FlaskForm):
    amount_req = FloatField('Cel')
    amount_avb = FloatField('Dostępne')
    account = SelectField('Konto', coerce=int)
    name = StringField('Nazwa Celu', validators=[Length(max=20)], render_kw={'placeholder': 'Nazwa Celu'})
    submitNewGoal = SubmitField('Dodaj')

class editGoalForm(FlaskForm):
    amount_req = FloatField('Cel')
    amount_avb = FloatField('Dostępne')
    account = SelectField('Konto', coerce=int)
    name = StringField('Nazwa Celu', validators=[Length(max=20)], render_kw={'placeholder': 'Nazwa Celu'})
    goal_id = StringField('goal_id')
    submitEditGoal = SubmitField('Zapisz')
    deleteGoal = SubmitField('Usuń')

class addIncTrForm(FlaskForm):
    tr_type_id = IntegerField('tr_type_id')
    tr_amount = FloatField('Kwota transakcji')
    tr_name = StringField('Nazwa Transakcji', validators=[Length(max=20)], render_kw={'placeholder': 'Nazwa Celu'})
    inc_category = SelectField('Kategoria')
    account = SelectField('Konto', coerce=int)
    tr_date = DateField('Data', default = datetime.now().date())
    tr_time = TimeField('Czas', default = datetime.now().time())
    submitNewTr = SubmitField('Dodaj')

class addExpTrForm(FlaskForm):
    tr_type_id = IntegerField('tr_type_id')
    tr_amount = FloatField('Kwota transakcji')
    tr_name = StringField('Nazwa Transakcji', validators=[Length(max=20)], render_kw={'placeholder': 'Nazwa Celu'})
    exp_category = SelectField('Kategoria')
    account = SelectField('Konto', coerce=int)
    tr_date = DateField('Data', default = datetime.now().date())
    tr_time = TimeField('Czas', default = datetime.now().time())
    submitNewTr = SubmitField('Dodaj')

class addTrfTrForm(FlaskForm):
    tr_type_id = IntegerField('tr_type_id')
    tr_amount = FloatField('Kwota transakcji')
    tr_name = StringField('Nazwa Transakcji', validators=[Length(max=20)], render_kw={'placeholder': 'Nazwa Celu'})
    account_f = SelectField('Konto Z', coerce=int)
    account_to = SelectField('Konto Do', coerce=int)
    tr_date = DateField('Data', default = datetime.now().date())
    tr_time = TimeField('Czas', default = datetime.now().time())
    submitNewTr = SubmitField('Dodaj')

class editTrForm(FlaskForm):
    tr_id = StringField('transaction_id')
    tr_amount = FloatField('Kwota transakcji')
    tr_name = StringField('Nazwa Transakcji', validators=[Length(max=20)], render_kw={'placeholder': 'Nazwa Celu'})
    inc_category = SelectField('Kategoria')
    tr_acc = StringField('account_id')
    tr_date = DateField('Data', default = datetime.now().date())
    tr_time = TimeField('Czas', default = datetime.now().time())
    submitEditTr = SubmitField('Zmień')
    deleteTr = SubmitField('Usuń')