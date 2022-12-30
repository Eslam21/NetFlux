
from flask import Flask, render_template , request , redirect , flash ,url_for, session

import mysql.connector
connection = mysql.connector.connect(user='SWE', password='123456789000',host='localhost',database='netflux')

cursor = connection.cursor()

app = Flask(__name__, static_folder='Front-End/static',template_folder="Front-End/templates")

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    massage=''
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        cursor.execute('SELECT * FROM persons WHERE userid=%s AND password=%s', (username, password))
        record = cursor.fetchone()
        if record != None:
            massage ="Login a Success!"
            return redirect(url_for('home'))
        else:
            massage ="Incorrect username or password. Try again!"
    return render_template('login.html', msg= massage)

@app.route("/registration", methods=["GET", "POST"])
def registration():
    massage=''
    if request.method == 'POST':

        firstname,lastname= request.form['name'].split(' ')
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirmPassword']
        gender = request.form['Gender']
        phone_number=request.form['phone_number']

        if password != confirmpassword:
            massage = 'The passwords do not match, please try again'
        else:
            try:
                cursor.execute('INSERT INTO persons (userid, first_name, last_name, email, password, gender,phone_number) VALUES (%s, %s, %s, %s, %s, %s,%s)', (username , firstname, lastname, email, password,gender,phone_number))
                connection.commit()
                massage = 'You have successfully registered !'
                return redirect(url_for('home'))
            except:
                massage = 'Account already exists !'
            
    return render_template('registration.html', msg= massage)


@app.route("/favorite" ,  methods=["GET", "POST"])
def favorite():
    return render_template('favorite.html')

@app.route("/history" ,  methods=["GET", "POST"])
def history():
    return render_template('history.html')

@app.route("/recommended" ,  methods=["GET", "POST"])
def recommended(): 
    return render_template('recommended.html')

@app.route("/watchlist" ,  methods=["GET", "POST"])
def watch_list():
    return render_template('watch_list.html')

@app.route("/profile-stat",  methods=["GET", "POST"])
def open_profile():
    return render_template('profile-stat.html')



if __name__ == "__main__":
    app.run(debug=True)


