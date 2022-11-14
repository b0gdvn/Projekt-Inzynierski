from capythal import db
from capythal.models import user, currency, card, acc_type, tr_type, style, category

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

db.session.commit()