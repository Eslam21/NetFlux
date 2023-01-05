from flask import Flask, render_template
import json

import mysql.connector
import requests
connection = mysql.connector.connect(user='SWE', password='123456789000',host='localhost',database='netflux')

cursor = connection.cursor()


app = Flask(__name__, static_folder='static',template_folder="templates")
@app.route('/')
@app.route("/home")
def home():
    
    cursor.execute("SELECT movieid FROM movies order by release_date desc limit 5")
    result=cursor.fetchall()
    
    ids=movies = [i[0] for i in result]
    for i in range(0,len(ids)):
        
        getResponse = requests.get(f'https://api.themoviedb.org/3/movie/{ids[i]}?api_key=c0bda0be71f7815fd6ba2eb5f5c86fd8')# every movie has a unique ID 
        getData = getResponse.json() # we request the data from the API and convert it to json
        getPath = "http://image.tmdb.org/t/p/w500" + getData['poster_path']
        ids[i]=getPath

    return render_template("image.html",path=ids)



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

@app.route('/temp')
def method_name():
    
    cursor.execute("select * from movies order by release_date desc ")
    movies=cursor.fetchall() 
    id = [i[0] for i in movies]
    title = [i[2] for i in movies]
    Overview = [i[3] for i in movies]
    path = [i[5] for i in movies]
    rating = [float(i[9]) for i in movies]
    
    return render_template("temp.html",title=title,Overview=Overview,path=path,rating=rating,movies=movies,id=id)

if __name__ == '__main__':
   
    app.run(debug=True)


