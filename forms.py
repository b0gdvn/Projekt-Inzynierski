from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class registrationForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=16)])
    user_name = StringField('Imię', validators=[DataRequired(), Length(min=1, max=30)])
    user_surname = StringField('Nazwisko', validators=[DataRequired(), Length(min=1, max=30)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Powtórz Hasło', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Zarejestruj Się')

class loginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj Się')