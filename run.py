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
            "SELECT password, person_type FROM persons WHERE userid=%s",
            (username,)
        )
        
        #fetch the hahsed password of the user
        result = cursor.fetchone()
       
        # check if this account exists and the password matches
        if result != None and bcrypt.checkpw(password,result[0].encode('utf-8')):
            session['username'] = username   #have the date here
            session['type'] =  result[1]
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
                session['type'] = 'user'
                return redirect(url_for("home"))
            except:
                msg = "Account already exists !"
                flash(msg)
                return redirect(url_for("registration")) 

    return render_template("registration.html")


@app.route("/liked", methods=["GET", "POST"])
def favorite():
    return render_template("home.html")


@app.route("/watched", methods=["GET", "POST"])
def history():
    return render_template("home.html")


@app.route("/recommend", methods=["GET", "POST"])
def recommended():
    return render_template("home.html")


@app.route("/watch_list", methods=["GET", "POST"])
def watch_list():
    return render_template("home.html")


@app.route("/profile-stat", methods=["GET", "POST"])
def open_stat():
    
    if session['type'] == 'admin':
        # number of total  movies
        cursor.execute("select count(*) from movies")
        no_of_movies = cursor.fetchone()[0]
        #number of users in database
        cursor.execute("select count(*) from persons WHERE person_type = 'user'")
        no_users = cursor.fetchone()[0]
        #number of males and females
        cursor.execute("select count(*) from persons WHERE person_type = 'user' AND gender = 'M' ")
        males = cursor.fetchone()[0]
         
        cursor.execute("select count(*) from persons WHERE person_type = 'user' AND gender = 'F' ")
        females = cursor.fetchone()[0]
        #top 5 popular movies 
        list_famous = [['movies', 'popularity']]
        cursor.execute("select title, popularity from movies ORDER BY popularity DESC lIMIT 10")
        list_famous.extend(cursor.fetchall())

        return render_template("profile-page-admin.html", popular_movies = list_famous ,no_of_movies = no_of_movies, no_users = no_users ,m = males, f= females )
        
    else:
        
        if request.method == "POST":
            if request.form['delete_account'] == "Delete Account":
                cursor.execute("delete from persons where userid=%s",(session['username'],))
                connection.commit()
                flash('Your account is deleted :(')
                
                return redirect(url_for("logout"))
        
        #country
        cursor.execute("select country from persons where userid=%s",(session['username'],))
        result_country=cursor.fetchone()[0]
        # films watched
        cursor.execute("select count(movieid) from watched where userid=%s",(session['username'],))
        result_count_watched=cursor.fetchone()[0]
        #number of favourites
        cursor.execute("select count(movieid) from favourites where userid=%s",(session['username'],))
        result_count_fav=cursor.fetchone()[0] 
        #total runtime
        cursor.execute("select sum(runtime) from movies where movieid in  (select movieid from watched where userid=%s) ",(session['username'],))
        count_runtime=cursor.fetchone()[0]
        #piechart
        all_movies = [['Genre', 'Number of Films']]
        cursor.execute("select genres, count(genres) from genres where movieid in  (select movieid from watched where userid=%s) group by genres HAVING COUNT(genres) > 1",(session['username'],))
        all_movies.extend(cursor.fetchall())

       

        return render_template("profile-stat.html",list_movies = all_movies ,count_runtime=count_runtime,count_fav = result_count_fav ,count_watched= result_count_watched, country=result_country )

@app.route("/profile-page", methods=["GET", "POST"])
def open_profile():
    alert=''
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
    
        if old_password_ == "" and new_password_ == "":
            cursor.execute(
            "UPDATE persons SET first_name = %s, last_name = %s , email=%s, birthday=%s, gender=%s, phone_number=%s,country=%s, city=%s, bio=%s WHERE userid=%s",
            (firstname_, lastname_, email_,birthday_, gender_, phonenumber_,country_, city_ , bio_  ,session['username']))
            connection.commit()
            flash("Updated Successfully")
            return redirect(url_for('open_profile'))
        else:
            old_password_ = old_password_.encode('utf-8')
            #check password
            cursor.execute("SELECT password FROM persons WHERE userid= %s", (session['username'],))
            result = cursor.fetchone()[0]
            if bcrypt.checkpw(old_password_ , result.encode('utf-8')):
                hashed_password = bcrypt.hashpw(new_password_.encode(), bcrypt.gensalt(rounds=12))
                cursor.execute(
                "UPDATE persons SET password = %s, first_name = %s, last_name = %s , email=%s, birthday=%s, gender=%s, phone_number=%s,country=%s, city=%s, bio=%s WHERE userid=%s",
                (hashed_password, firstname_, lastname_, email_,birthday_, gender_, phonenumber_,country_, city_ , bio_  ,session['username']))
                connection.commit()
                flash("Updated Successfully")
            else:
               flash("Incorrect password, please try again")
            return redirect(url_for('open_profile'))
  
    return render_template("profile-page.html", a = alert ,first_name=first_name, last_name= last_name, email=email, birthday=birthday, gender=gender, phonenumber=phonenumber,country=country, city=city, bio=bio)



if __name__ == "__main__":
    app.run(debug=True)
