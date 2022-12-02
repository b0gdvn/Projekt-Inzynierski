from capythal import db
from capythal.models import user, currency, card, acc_type, tr_type, style, category, account, transaction
from random import randint
from datetime import datetime, time

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
exp_icon = ['shirt', 'utensils', 'bus', 'car', 'house', 'icons', 'child-reaching', 'map-location-dot', 'suitcase-medical', 'hand-sparkles', 'desktop', 'phone-volume', 'user-graduate', 'ellipsis' ]

for n, (exp, ico) in enumerate(zip(exp_categories, exp_icon), start=1):
    db.session.add(category(style_id=n%len(colors), tr_type_id=1, name=exp, icon=ico))

inc_categories = ['Wynagrodzenie', 'Premia', 'Sprzedaż', 'Inne']
inc_icon = ['money-check-dollar', 'money-bill-1-wave', 'clipboard-check', 'ellipsis' ]

for n, (inc, ico) in enumerate(zip(inc_categories, inc_icon), start=1):
    db.session.add(category(style_id=n, tr_type_id=2, name=inc, icon=ico))

db.session.add(account(user_id=1, amount=3221.21, currency_id=1, card_id=3, acc_type_id=2, style_id=randint(1,10), card_number='2211', fin_inst='PeKaO'))
db.session.add(account(user_id=1, amount=424.00, currency_id=1, card_id=2, acc_type_id=1, style_id=randint(1,10), card_number='1234', fin_inst='Santander'))
db.session.add(account(user_id=1, amount=5392.39, currency_id=2, card_id=1, acc_type_id=3, style_id=randint(1,10), fin_inst='XTB'))
db.session.add(account(user_id=1, amount=213.90, currency_id=3, card_id=2, acc_type_id=2, style_id=randint(1,10), card_number='3322', fin_inst='GetIn Bank'))
db.session.add(account(user_id=1, amount=3412.36, currency_id=1, card_id=1, acc_type_id=4, style_id=randint(1,10)))

db.session.add(transaction(account_id=2, category_id=2, tr_type_id=1, name='McDonalds', amount=24.50, date=datetime.strptime('2022-11-22', '%Y-%m-%d'), time=datetime.strptime('18:34:00', '%H:%M:%S').time()))
db.session.add(transaction(account_id=2, category_id=1, tr_type_id=1, name='H&M koszulka', amount=69.90, date=datetime.strptime('2022-11-22', '%Y-%m-%d'), time=datetime.strptime('14:03:00', '%H:%M:%S').time()))
db.session.add(transaction(account_id=2, category_id=15, tr_type_id=2, name='Wynagrodzenie Miesięczne', amount=4670.29, date=datetime.strptime('2022-11-21', '%Y-%m-%d'), time=datetime.strptime('19:52:00', '%H:%M:%S').time()))
db.session.add(transaction(account_id=2, category_id=4, tr_type_id=1, name='Opony Zimowe', amount=799.00, date=datetime.strptime('2022-11-21', '%Y-%m-%d'), time=datetime.strptime('14:13:00', '%H:%M:%S').time()))
db.session.add(transaction(account_id=2, category_id=2, tr_type_id=1, name='KFC', amount=12.50, date=datetime.strptime('2022-11-21', '%Y-%m-%d'), time=datetime.strptime('09:56:00', '%H:%M:%S').time()))

db.session.commit()