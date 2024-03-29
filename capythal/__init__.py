from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_caching import Cache


app=Flask(__name__)

# Inicjalizacja Cache
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

# Klucz autentyfikacji
app.config['SECRET_KEY'] = 'd91fa1479fcdb3eaa587fd43f44ea668'

# Baza danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///capythal.db'
db = SQLAlchemy(app)

# Szyfrowanie haseł
bcrypt = Bcrypt(app)

# Logowanie
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from capythal import routes