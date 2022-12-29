
from flask import Flask, render_template , request , redirect , flash ,url_for, session

import mysql.connector
connection = mysql.connector.connect(user='root', password='Storemagic2002$',host='localhost',database='netflux')

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
        cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))
        record = cursor.fetchone()
        if record != None:
            #create a session 
            #session['loggedin'] = True
            #session['username'] = record['username']
            massage ="Login a Success!"
            return redirect(url_for('home'))
        else:
            massage ="Incorrect username or password. Try again!"
            print(massage)
    
    return render_template('login.html', msg= massage)



@app.route("/registration", methods=["GET", "POST"])
def registration():
    ''''
    massage=''
    if request.method == 'POST':
        fullname = request.form['name']
        firstname = fullname.split(' ')[0]
        secondname = fullname.split(' ')[0]
        username = request.form['username']
        email = request.form['email']
        phonenumber = request.form['number']
        password = request.form['password']
        confirmpassword = request.form['confirmPassword']
        gender = request.form['Gender']
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        else:
            cursor.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)', (username , firstname, secondname, email, password,gender ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    '''
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

@app.route("/watch_list" ,  methods=["GET", "POST"])
def watch_list():
    return render_template('watch_list.html')

@app.route("/profile-page",  methods=["GET", "POST"])
def open_profile():
    return render_template('profile-page.html')

if __name__ == "__main__":
    app.run(debug=True)


