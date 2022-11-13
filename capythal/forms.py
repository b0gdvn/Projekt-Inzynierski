from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from capythal.models import user

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

    def __getitem__(self, key):
        return self.__dict__[key]