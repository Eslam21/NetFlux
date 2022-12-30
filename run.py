from flask import Flask, render_template, request, redirect, flash, url_for, session
import bcrypt
import mysql.connector

connection = mysql.connector.connect(
    user="SWE", password="123456789000", host="localhost", database="netflux"
)

cursor = connection.cursor()

#flash uses secret key

app = Flask(__name__, static_folder='Front-End/static',template_folder="Front-End/templates")
app.secret_key = 'keep the secret!'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["Username"]
        #password the user entered, still needs to be checked
        password = request.form["Password"].encode('utf-8')
        cursor.execute(
            "SELECT password FROM persons WHERE userid=%s",
            (username,)
        )
        
        #fetch the hahsed password of the user
        result = cursor.fetchone()
       
        # check if this account exists and the password matches
        if result != None and bcrypt.checkpw(password,result[0].encode('utf-8')):
            return redirect(url_for("home"))
        
        else:
            msg = "Incorrect username or password. Try again!"
            flash(msg)
            
    return render_template("login.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    msg = ""
    if request.method == "POST":

        firstname, lastname = request.form["name"].split(" ")
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirmpassword = request.form["confirmPassword"]
        gender = request.form["Gender"]
        phone_number = request.form["phone_number"]
    

        if password != confirmpassword:
            msg = "The passwords do not match, please try again"
            flash(msg)
        else:
            try:
                # Hash a password for the first time, with a randomly-generated salt
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
                cursor.execute(
                    "INSERT INTO persons (userid, first_name, last_name, email, password, gender,phone_number) VALUES (%s, %s, %s, %s, %s, %s,%s)",
                    (
                        username,
                        firstname,
                        lastname,
                        email,
                        hashed_password,
                        gender,
                        phone_number,
                    ),
                )
                connection.commit()
                msg = "You have successfully registered !"
                return redirect(url_for("home"))
            except:
                msg = "Account already exists !"
                flash(msg)

    return render_template("registration.html")


@app.route("/favorite", methods=["GET", "POST"])
def favorite():
    return render_template("favorite.html")


@app.route("/history", methods=["GET", "POST"])
def history():
    return render_template("history.html")


@app.route("/recommended", methods=["GET", "POST"])
def recommended():
    return render_template("recommended.html")


@app.route("/watchlist", methods=["GET", "POST"])
def watch_list():
    return render_template("watch_list.html")


@app.route("/profile-stat", methods=["GET", "POST"])
def open_profile():
    return render_template("profile-stat.html")


if __name__ == "__main__":
    app.run(debug=True)
