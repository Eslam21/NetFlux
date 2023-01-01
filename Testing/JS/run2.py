from flask import Flask, render_template
import json

import mysql.connector
connection = mysql.connector.connect(user='root', password='Storemagic2002$',host='localhost',database='netflux')

cursor = connection.cursor()


app = Flask(__name__)

@app.route('/')
@app.route("/home")
def home():
    return render_template("image.html")



@app.route("/visualize")
def hello_world():

    '''
    xValues = ["Italy", "France", "Spain", "USA", "Argentina","Mystical"]
    yValues = [55, 49, 44, 24, 15,100]
    '''

   

    cursor.execute('SELECT title, vote_average FROM movies LIMIT 5')
    result = cursor.fetchall()

    movies = [i[0] for i in result]
    vote_average = [float(i[1]) for i in result]
    barColors = ["red", "green","blue","orange","brown","purple"]
    
    #cursor.execute('SELECT * FROM users WHERE username=%s AND password=%s', (username, password))

    return render_template("visualize.html", movies = movies, vote_average = vote_average, barColors = barColors)


if __name__ == '__main__':
   
    app.run(debug=True)


