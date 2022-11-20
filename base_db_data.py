from capythal import db
from capythal.models import user, currency, card, acc_type, tr_type, style, category, account
from random import randint
# UWAGA! Uruchomnienie tego kodu usunie wszystkie rekordy użytkowników istniejące wcześniej

db.drop_all()
db.create_all()

currencies = ['PLN', 'USD', 'EUR', 'GBP', 'BTC']

for c in currencies:
    db.session.add(currency(name=c))

cards = ['', 'MasterCard', 'Visa', 'Inna']

for c in cards:
    db.session.add(card(name=c))

acc_types = ['Rachunek Bieżący', 'Karta Kredytowa', 'Konto Maklerskie', 'Gotówka', 'Inne']

for a in acc_types:
    db.session.add(acc_type(name=a))

tr_types = ['Wydatek', 'Przychód']

for t in tr_types:
    db.session.add(tr_type(name=t))

colors = ['red', 'blue', 'cyan', 'green', 'grey', 'lime', 'orange', 'pink', 'violet', 'yellow']
colors_pl = ['Czerwony', 'Niebieski', 'Turkusowy', 'Zielony', 'Szary', 'Limonkowy', 'Pomarańczowy', 'Różowy', 'Fioletowy', 'Żółty']

for c, pl in zip(colors, colors_pl):
    db.session.add(style(name=c, name_pl=pl))

exp_categories = ['Odzież', 'Jedzenie', 'Transport', 'Samochód', 'Dom', 'Rozrywka', 'Dzieci', 'Podróżowanie', 'Zdrowie', 'Wygląd', 'Urządzenia', 'Komunikacja', 'Edukacja', 'Inne']

for n, e in enumerate(exp_categories):
    db.session.add(category(style_id=n%len(colors), tr_type_id=1, name=e))

inc_categories = ['Wynagrodzenie', 'Premia', 'Sprzedaż', 'Inne']

for n, i in enumerate(inc_categories):
    db.session.add(category(style_id=n, tr_type_id=2, name=i))

db.session.add(account(user_id=1, amount=3221.21, currency_id=1, card_id=3, acc_type_id=2, style_id=randint(1,10), card_number='2211', fin_inst='PeKaO'))
db.session.add(account(user_id=1, amount=424.00, currency_id=1, card_id=2, acc_type_id=1, style_id=randint(1,10), card_number='1234', fin_inst='Santander'))
db.session.add(account(user_id=1, amount=5392.39, currency_id=2, card_id=1, acc_type_id=3, style_id=randint(1,10), fin_inst='XTB'))
db.session.add(account(user_id=1, amount=213.90, currency_id=3, card_id=2, acc_type_id=2, style_id=randint(1,10), card_number='3322', fin_inst='GetIn Bank'))
db.session.add(account(user_id=1, amount=3412.36, currency_id=1, card_id=1, acc_type_id=4, style_id=randint(1,10)))

db.session.commit()