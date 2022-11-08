from flask import Flask, render_template
import os

app=Flask(__name__)

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/stats')
def stats():
    return render_template("stats.html")
    
@app.route('/accounts')
def accounts():
    return render_template("accounts.html")

@app.route('/goals')
def goals():
    return render_template("goals.html")

@app.route('/history')
def history():
    return render_template("history.html")

if __name__=="__main__":
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 4444)))