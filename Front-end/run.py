create_table_user = "CREATE TABLE user (UserID INT(10) NOT NULL AUTO_INCREMENT,FristName VARCHAR(20) NOT NULL,LastName VARCHAR(20) DEFAULT NULL,Username VARCHAR(20) NOT NULL,Email VARCHAR(30) NOT NULL,PhoneNumber VARCHAR(11) NOT NULL,Password VARCHAR(20) NOT NULL,Gender VARCHAR(6) NOT NULL,PRIMARY KEY (USERID));"

from flask import Flask, render_template , request , redirect
import pymysql
import database_detail

conn = pymysql.connect(
    host = database_detail.host,
    user = database_detail.user,
    password =database_detail.password,
    db = database_detail.db
    )




app = Flask(__name__, static_folder='static')


try:
    cursor = conn.cursor()
    cursor.execute(create_table_user)
except pymysql.err.OperationalError:
    pass



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="POST":
        print(request.form)

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
    return render_template('login.html')

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method=="POST":
        # print(request.form)
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
    return render_template('registration.html')


if __name__ == "__main__":
    app.run(debug=True)
