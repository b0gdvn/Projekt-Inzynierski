from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

# Klucz autentyfikacji
app.config['SECRET_KEY'] = 'd91fa1479fcdb3eaa587fd43f44ea668'

# Baza danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capythal.db'
db = SQLAlchemy(app)

from capythal import routes