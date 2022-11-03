from cProfile import run
from flask import Flask, render_template

app=Flask(__name__)

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/accounts')
def accounts():
    return render_template("accounts.html")

if __name__=="__main__":
    app.run(debug=True)