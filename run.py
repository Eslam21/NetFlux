from flask import Flask, render_template , request , redirect , flash

import mysql.connector
mydb = mysql.connector.connect(user='root', password='147258369',
                              host='127.0.0.1',
                              database='netflux')

mycursor = mydb.cursor()

app = Flask(__name__, static_folder='Front-End/static',template_folder="Front-End/templates")

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    
    return render_template('login.html')


@app.route("/registration", methods=["GET", "POST"])
def registration():
   
    return render_template('registration.html')


@app.route("/favorite")
def favorite():
    return render_template('favorite.html')

@app.route("/history")
def history():
    return render_template('history.html')

@app.route("/recommended")
def recommended():
    return render_template('recommended.html')

@app.route("/watch_list")
def watch_list():
    return render_template('watch_list.html')

if __name__ == "__main__":
    app.run(debug=True)
