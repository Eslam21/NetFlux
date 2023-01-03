from flask import Flask, render_template, request, redirect, flash, url_for, session
import bcrypt
import mysql.connector
import datetime

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
            session['username'] = username   #have the date here 
            return redirect(url_for("home"))
        
        else:
            msg = "Incorrect username or password. Try again!"
            flash(msg)
            return redirect(url_for("login"))
            
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop('username', None)   
    return render_template("home.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    msg = ""
    if request.method == "POST":

        firstname = request.form["fname"]
        lastname = request.form["lname"]
        username = request.form["username"]
        birthday = request.form["Birthday"]
        email = request.form["email"]
        password = request.form["password"]
        confirmpassword = request.form["confirmPassword"]
        gender = request.form["Gender"]
        phone_number = request.form["phone_number"]
    


        if password != confirmpassword:
            msg = "The passwords do not match, please try again"
            flash(msg)
            return redirect(url_for("registration")) 
        else:
            try:
                # Hash a password for the first time, with a randomly-generated salt
                hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
                cursor.execute(
                    "INSERT INTO persons (userid, first_name, last_name, email, password, gender,phone_number, birthday) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)",
                    (
                        username,
                        firstname,
                        lastname,
                        email,
                        hashed_password,
                        gender,
                        phone_number,
                        birthday,
                    ),
                )
                connection.commit()
                msg = "You have successfully registered !"
                session['username'] = username 
                return redirect(url_for("home"))
            except:
                msg = "Account already exists !"
                flash(msg)
                return redirect(url_for("registration")) 

    return render_template("registration.html")


@app.route("/favorite", methods=["GET", "POST"])
def favorite():
    return render_template("home.html")


@app.route("/history", methods=["GET", "POST"])
def history():
    return render_template("home.html")


@app.route("/recommended", methods=["GET", "POST"])
def recommended():
    return render_template("home.html")


@app.route("/watchlist", methods=["GET", "POST"])
def watch_list():
    return render_template("home.html")


@app.route("/profile-stat", methods=["GET", "POST"])
def open_stat():
    return render_template("profile-stat.html")

@app.route("/profile-page", methods=["GET", "POST"])
def open_profile():
    
    #show the information in the database 
    cursor.execute(
            "SELECT first_name, last_name, email, password, birthday, gender, phone_number,country, city, bio FROM persons WHERE userid=%s",
            (session['username'],)
        )
    result = cursor.fetchone()
    
    first_name = result[0]
    last_name = result[1]
    email = result[2]
    birthday = result[4]
    gender = result[5]
    phonenumber = result[6]
    country = result[7]
    city = result[8]
    bio = result[9]
    if request.method == "POST":
        #userid_ = request.form["username"]
        firstname_ = request.form["firstname"]
        lastname_ = request.form["lastname"]
        email_ = request.form["email"]
        birthday_ = request.form["birthday"]
        gender_ = request.form["gender"]
        phonenumber_ = request.form["phonenumber"]
        country_ = request.form["country"]
        city_= request.form["city"]
        bio_= request.form["bio"]

        old_password_ = request.form["oldpassword"]
        new_password_ = request.form["newpassword"]

        cursor.execute(
        "UPDATE persons SET first_name = %s, last_name = %s , email=%s, birthday=%s, gender=%s, phone_number=%s,country=%s, city=%s, bio=%s WHERE userid=%s",
        (firstname_, lastname_, email_,birthday_, gender_, phonenumber_,country_, city_ , bio_  ,session['username']))
        connection.commit()
           
        
    return render_template("profile-page.html", first_name=first_name, last_name= last_name, email=email, birthday=birthday, gender=gender, phonenumber=phonenumber,country=country, city=city, bio=bio)


if __name__ == "__main__":
    app.run(debug=True)
