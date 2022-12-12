create_table_user = """
CREATE TABLE IF NOT EXISTS user (
	UserID INT NOT NULL AUTO_INCREMENT UNIQUE,
    FristName VARCHAR(20) NOT NULL,
    LastName VARCHAR(20) DEFAULT NULL,
    Username VARCHAR(20) NOT NULL UNIQUE,
    Email VARCHAR(30) NOT NULL UNIQUE,
    PhoneNumber VARCHAR(11) NOT NULL UNIQUE,
    Password VARCHAR(20) NOT NULL,
    Gender VARCHAR(6) NOT NULL,
    PRIMARY KEY (USERID));
"""

from flask import Flask, render_template , request , redirect , flash
import pymysql
import database_detail
from waitress import serve

conn = pymysql.connect(
    host = database_detail.host,
    user = database_detail.user,
    password =database_detail.password,
    db = database_detail.db
    )


app = Flask(__name__, static_folder='static')
app.secret_key = 'super secret key LOL'

cursor = conn.cursor()
cursor.execute(create_table_user)



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        # print(request.form)

        cursor.execute("SELECT COUNT(Username) FROM user WHERE username = %s AND password = %s LIMIT 0, 1;",
            (
                request.form.get("Username"),
                request.form.get("Password")
            )
        )
        conn.commit()
        result=cursor.fetchone()
        if(result == (1,)):
            return redirect('/home')
        else:
            flash("Incorrect Email or Password")
    return render_template('login.html')


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method=="POST":
            
        try:
            cursor.execute("INSERT INTO user (FristName,LastName,Username,Email,PhoneNumber,Password,Gender) VALUES (%s,%s,%s,%s, %s, %s, %s);",
                (
                    request.form.get("name").split(" ")[0],
                    request.form.get("name").split(" ")[1],
                    request.form.get("username"),
                    request.form.get("email"),
                    request.form.get("number"),
                    request.form.get("password"),
                    request.form.get("Gender")
                )
            )   
            conn.commit()
            return redirect('/home')
        except pymysql.err.IntegrityError:
            flash("Username or Email already Exists")
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
    serve(app, host="127.0.0.1", port=5000)
