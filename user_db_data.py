from capythal import db
from capythal.models import account

from random import randint

#sprawdzić czy card id 1 jest przydatny (null value zamiast tego)

db.session.add(account(user_id=1, currency_id=1, card_id=2, acc_type_id=1, style_id=randint(1,10), card_number='1234', fin_inst='Santander'))
db.session.add(account(user_id=1, currency_id=1, card_id=3, acc_type_id=2, style_id=randint(1,10), card_number='2211', fin_inst='PeKaO'))
db.session.add(account(user_id=1, currency_id=2, card_id=1, acc_type_id=3, style_id=randint(1,10), fin_inst='XTB'))
db.session.add(account(user_id=1, currency_id=3, card_id=2, acc_type_id=2, style_id=randint(1,10), card_number='3322', fin_inst='GetIn Bank'))
db.session.add(account(user_id=1, currency_id=1, card_id=1, acc_type_id=4, style_id=randint(1,10)))

db.session.commit()